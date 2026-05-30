import requests

def fetch_account_id(api_key, platform):
    """
    Fetch the account ID for a given platform from Zernio API.
    
    Args:
        api_key (str): The Zernio API key
        platform (str): The platform name (e.g., 'instagram', 'youtube')
        
    Returns:
        str: The account ID (_id field) of the first account
        
    Raises:
        Exception: If the API request fails with a non-200 status code
    """
    url = f"https://api.zernio.com/v1/accounts?platform={platform}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status code: {response.status_code}")
    
    data = response.json()
    
    # Return the _id of the first account
    return data[0]["_id"]