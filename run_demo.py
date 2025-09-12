# run_demo.py

from controlled_generation import generate_valid_json

if __name__ == "__main__":
    initial_prompt =  "I'm currently configuring a wireless access point for our office network and I need to generate a JSON object that accurately represents its settings. The access point's SSID should be 'OfficeNetSecure', it uses WPA2-Enterprise as its security protocol, and it's capable of a bandwidth of up to 1300 Mbps on the 5 GHz band. This JSON object will be used to document our network configurations and to automate the setup process for additional access points in the future. Please provide a JSON object that includes these details." # Start from an opening brace
    final_output = generate_valid_json(prompt=initial_prompt)
    print("\nFinal JSON output:\n", final_output)
