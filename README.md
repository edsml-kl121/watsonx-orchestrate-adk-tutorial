Install and create a virtual environment from `requirement.txt`

```
python -m venv venv
source venv/bin/acitvate
uv pip install -r requirement.txt
```

For AWS Saas
```
orchestrate env list
orchestrate env add -n test-env -u <Service instance URL>
orchestrate env activate test-env
(Then enter API Key)
```
