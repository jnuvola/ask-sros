

<h1><img src="https://github.com/user-attachments/assets/dd1effb6-0545-41ad-b620-30785ed5f291" width="30" height="30" alt="ask-sros-ico" style="vertical-align: middle;"> Ask SR OS</h1>
A simplistic Python+Flask MVP implementation that harnesses MLL reasoning to interpret user network questions into Nokia SR OS command and return the answer.

## Usage
### 1. Install Dependencies  
Ensure you have Python installed, then run:  
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables  
Set the following environment variables before running the application:  

```bash
export OPENAI_API_KEY="<your-api-key>"
export OPENAI_MODEL_NAME="gpt-4o"
export ASKSROS_ROUTER_ADDRESS="10.10.10.1"
export ASKSROS_ROUTER_PORT="22"
export ASKSROS_ROUTER_USERNAME="admin"
export ASKSROS_ROUTER_PASSWORD="admin"
```

### 3. Run the Application  
Start the Flask server with:  
```bash
python ask-sros.py
```

## Demo

![asksros-demo](https://github.com/user-attachments/assets/7fcef869-c18f-4e00-a0f6-1dee06c7da03)
