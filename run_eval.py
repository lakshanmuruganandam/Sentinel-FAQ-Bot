import requests
import time
import subprocess
import os

print("--- INITIATING TASK 2: FAQ CHATBOT EVALUATION ---")

# Boot server
proc = subprocess.Popen(["python", "main.py"], cwd=os.path.dirname(os.path.abspath(__file__)))

# Poll until ready
ready = False
for _ in range(15):
    try:
        res = requests.get("http://localhost:8002/", timeout=1)
        if res.status_code == 200:
            ready = True
            break
    except:
        time.sleep(0.8)

if not ready:
    print("❌ Failed to start server.")
    proc.terminate()
    exit(1)

try:
    # 1. UI Check
    res = requests.get("http://localhost:8002/")
    print(f"GET / -> Status: {res.status_code}, Length: {len(res.text)} bytes")
    assert res.status_code == 200

    # 2. FAQs Index Endpoint Check
    res = requests.get("http://localhost:8002/api/faqs")
    data = res.json()
    print(f"GET /api/faqs -> Indexed FAQs: {data['total']}")
    assert data["total"] >= 8

    # 3. Test Matching Matrix
    queries = [
        "What is Sentinel AI?",
        "How do I reset my password?",
        "What are the pricing options?",
        "Is my data GDPR secure?",
        "Can I install via pip?",
        "What is the airspeed velocity of an unladen swallow?" # Expected fallback
    ]

    for q in queries:
        start = time.time()
        res = requests.post("http://localhost:8002/api/chat", json={"question": q})
        elapsed = (time.time() - start) * 1000
        d = res.json()
        print(f"  Q: '{q}' => Conf: {d.get('confidence')}% | Matched: {d.get('matched')} ({elapsed:.1f}ms)")
        assert d.get("status") == "success"

    # 4. Add Dynamic FAQ Test
    add_res = requests.post("http://localhost:8002/api/faqs/add", json={
        "category": "Testing",
        "question": "Does Task 2 pass all automated benchmarks?",
        "answer": "Yes, Task 2 Sentinel FAQ Bot achieves 100% test accuracy."
    })
    add_d = add_res.json()
    print(f"\nPOST /api/faqs/add -> Status: {add_res.status_code}, Msg: {add_d.get('message')}")
    assert add_d.get("status") == "success"

    print("\n✅ TASK 2 EVALUATION: 100% SUCCESS")

finally:
    proc.terminate()
