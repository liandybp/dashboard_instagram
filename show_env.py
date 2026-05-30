#!/usr/bin/env python3

import os

def main():
    env_file = '.env'
    
    if not os.path.exists(env_file):
        print("Error: .env file not found")
        return
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Truncate API keys for display
    lines = content.strip().split('\n')
    truncated_lines = []
    
    for line in lines:
        if line.startswith('ZERNIO_API_KEY=') or line.startswith('ANTHROPIC_API_KEY='):
            key, value = line.split('=', 1)
            # Show only first 4 and last 4 characters of the API key
            if len(value) > 8:
                truncated_value = value[:4] + '*' * (len(value) - 8) + value[-4:]
                truncated_lines.append(f"{key}={truncated_value}")
            else:
                truncated_lines.append(line)
        else:
            truncated_lines.append(line)
    
    print("Current .env file contents (API keys truncated for security):")
    print('\n'.join(truncated_lines))

if __name__ == "__main__":
    main()