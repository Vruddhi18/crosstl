import pytest
from typing import List
from crosstl.backend.DirectX.DirectxLexer import HLSLLexer


def tokenize_code(code: str) -> List:
    """Helper function to tokenize code."""
    lexer = HLSLLexer(code)
    return lexer.tokens


def test_struct_tokenization():
    code = """
    struct VSInput {
        float4 position : SV_position;
        float4 color : TEXCOORD0;
    };

    struct VSOutput {
        float4 out_position : TEXCOORD0;
    };
    """
    try:
        tokenize_code(code)
    except SyntaxError:
        pytest.fail("struct tokenization not implemented.")


def test_if_tokenization():
    code = """
    VSOutput VSMain(VSInput input) {
        VSOutput output;
        output.out_position = input.position;
        if (input.color.r > 0.5) {
            output.out_position = input.color;
        }
        return output;
    }
    """
    try:
        tokenize_code(code)
    except SyntaxError:
        pytest.fail("if tokenization not implemented.")


def test_for_tokenization():
    code = """
    VSOutput VSMain(VSInput input) {
        VSOutput output;
        for (int i = 0; i < 10; i++) {
            output.out_position += input.position;
        }
        return output;
    }
    """
    try:
        tokenize_code(code)
    except SyntaxError:
        pytest.fail("for tokenization not implemented.")


def test_else_tokenization():
    code = """
    PSOutput PSMain(PSInput input) {
        PSOutput output;
        if (input.in_position.r > 0.5) {
            output.out_color = input.in_position;
        } else {
            output.out_color = float4(0.0, 0.0, 0.0, 1.0);
        }
        return output;
    }
    """
    try:
        tokenize_code(code)
    except SyntaxError:
        pytest.fail("else tokenization not implemented.")


def test_function_call_tokenization():
    code = """
    PSOutput PSMain(PSInput input) {
        PSOutput output;
        output.out_color = saturate(input.in_position);
        return output;
    }
    """
    try:
        tokenize_code(code)
    except SyntaxError:
        pytest.fail("Function call tokenization not implemented.")


def test_else_if_tokenization():
    code = """
    PSOutput PSMain(PSInput input) {
        PSOutput output;
        if (input.in_position.r > 0.5) {
            output.out_color = input.in_position;
        } else if (input.in_position.r == 0.5){
            output.out_color = float4(1.0, 1.0, 1.0, 1.0);
        } else {
            output.out_color = float4(0.0, 0.0, 0.0, 1.0);
        }
        return output;
    }
    """
    try:
        tokenize_code(code)
    except SyntaxError:
        pytest.fail("else_if tokenization not implemented.")


def test_assignment_ops_tokenization():
    code = """
    PSOutput PSMain(PSInput input) {
        PSOutput output;
        output.out_color = float4(0.0, 0.0, 0.0, 1.0);

        if (input.in_position.r > 0.5) {
            output.out_color += input.in_position;
        }

        if (input.in_position.r < 0.5) {
            output.out_color -= float4(0.1, 0.1, 0.1, 0.1);
        }

        if (input.in_position.g > 0.5) {
            output.out_color *= 2.0;
        }

        if (input.in_position.b > 0.5) {
            output.out_color /= 2.0;
        }

        // Testing SHIFT_LEFT (<<) operator on some condition
        if (input.in_position.r == 0.5) {
            uint redValue = asuint(output.out_color.r);
            output.redValue ^= 0x1;
            output.out_color.r = asfloat(redValue);
            output.redValue |= 0x2;

            // Applying shift left operation
            output.redValue << 1; // Shift left by 1
            redValue |= 0x2;

            redValue &= 0x3;
        }
        
        // Testing SHIFT RIGHT (>>) operator on some condition
        if (input.in_position.r == 0.25) {
            uint redValue = asuint(output.out_color.r);
            output.redValue ^= 0x1;
            output.out_color.r = asfloat(redValue);
            output.redValue |= 0x2;

            // Applying shift left operation
            output.redValue >> 1; // Shift left by 1
            redValue |= 0x2;

            redValue &= 0x3;
        }


        return output;
    }
    """
    try:
        tokenize_code(code)
    except SyntaxError:
        pytest.fail("assign_op tokenization is not implemented.")


def test_bitwise_or_tokenization():
    code = """
        uint val = 0x01;
        val = val | 0x02;
    """
    try:
        tokenize_code(code)
    except SyntaxError:
        pytest.fail("bitwise_op tokenization is not implemented.")


if __name__ == "__main__":
    pytest.main()
