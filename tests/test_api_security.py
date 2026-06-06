from anaya.api.security import sign_webhook_body, verify_webhook_signature


def test_webhook_signature_round_trip():
    body = b'{"zen":"Keep it logically awesome."}'
    signature = sign_webhook_body(body, "secret")

    assert signature.startswith("sha256=")
    assert verify_webhook_signature(body, signature, "secret")
    assert not verify_webhook_signature(body, signature, "wrong")
    assert not verify_webhook_signature(body, "sha1=bad", "secret")
