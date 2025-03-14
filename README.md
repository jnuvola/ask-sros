<div style="display: flex; align-items: left; justify-content: left;">
  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 10px;">
    <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#4cc9f0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M2 17L12 22L22 17" stroke="#4cc9f0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M2 12L12 17L22 12" stroke="#4cc9f0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
  <h1>Ask SR OS</h1>
</div>

A simplistic Python+Flask MVP that harnesses MLL reasoning to interpret user network questions into Nokia SR OS commands and return the answer.

## Usage
### Install Dependencies  
Ensure you have Python installed, then run:  
```bash
pip install -r requirements.txt
```

### Configure Environment Variables  
Set the following environment variables before running the application:  

```bash
export OPENAI_API_KEY="<your-api-key>"
export OPENAI_MODEL_NAME="gpt-4o"
export ASKSROS_ROUTER_ADDRESS="10.10.10.1"
export ASKSROS_ROUTER_PORT="22"
export ASKSROS_ROUTER_USERNAME="admin"
export ASKSROS_ROUTER_PASSWORD="admin"
```

### Run the Application  
Start the Flask server with:  
```bash
python ask-sros.py
```
