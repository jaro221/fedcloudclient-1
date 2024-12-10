from fedcloudclient.checkin import *

if __name__ == "__main__":
    print(f"Start of verifying master branch.py")


    access_token=get_access_token(None,"jaro221",None,None)

    oidc_url_pre = decode_token(access_token)
    oidc_url=oidc_url_pre["iss"]
    oidc_ep = oidc_discover(oidc_url)
    z_user_info=oidc_ep["userinfo_endpoint"]
    z_head={"Authorization": f"Bearer {access_token}"}
    
    request = requests.get(
        oidc_ep["userinfo_endpoint"],
        headers={"Authorization": f"Bearer {access_token}"},
    )

    request.raise_for_status()
    vos = set()
    pattern = re.compile(VO_PATTERN)
    for claim in request.json().get("eduperson_entitlement", []):
        vo = pattern.match(claim)
        if vo:
            vos.add(vo.groups()[0])

    print(f"Break")