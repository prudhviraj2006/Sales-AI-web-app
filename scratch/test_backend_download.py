import requests
import os

def test_download():
    job_id = "job_20260508032924_a494e9a9"
    url = f"http://127.0.0.1:8000/api/download?job_id={job_id}&format=pdf"
    
    print(f"Requesting PDF for job {job_id}...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Success! PDF received. Size: {len(response.content)} bytes")
            with open("scratch/test_download.pdf", "wb") as f:
                f.write(response.content)
            print("PDF saved to scratch/test_download.pdf")
        else:
            print(f"Failed! Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_download()
