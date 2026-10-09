import hmac, hashlib, base64


def is_valid_shopify_signature(body, signature, secret):
    key_bytes = secret.encode("utf-8")
    digest_bytes = hmac.new(key_bytes, body, hashlib.sha256).digest()
    base64_bytes = base64.b64encode(digest_bytes)
    expected_signature = base64_bytes.decode()
    return hmac.compare_digest(expected_signature, signature)


if __name__ == "__main__":
    body = b'{"customer": null}'
    good = "wFz18mlz20VUx4h/B0qmf3VrCV/DBp/zmLe6b6Krsjw="
    print(is_valid_shopify_signature(body, good, "testsecret"))
    print(is_valid_shopify_signature(b'{"customer": 1}', good, "testsecret"))
    print(is_valid_shopify_signature(body, good, "wrongsecret"))