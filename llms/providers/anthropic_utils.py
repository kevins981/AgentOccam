# Use the native inference API to send a text message to Anthropic Claude.

import boto3
import json

def generate_from_anthropic_completion(
    prompt: str,
    engine: str,
) -> str:
    # Create a Bedrock Runtime client in the AWS Region of your choice.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Set the model ID, e.g., Claude 3 Haiku.
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    # Format the request payload using the model's native structure.
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        response = client.invoke_model(modelId=engine, body=request)

    except Exception as e: # (ClientError, Exception) as e:
        raise KeyError(f"ERROR: Can't invoke '{engine}'. Reason: {e}")

    # Decode the response body.
    model_response = json.loads(response["body"].read())

    # Extract and print the response text.
    response_text = model_response["content"][0]["text"]

    return response_text