const MIN_USERNAME_LENGTH = 4;
const MIN_FULL_NAME_LENGTH = 3;
const MIN_PASSWORD_LENGTH = 8;

const keys = {
    "msg": ["msg"],
    "register": ["msg", "id"],
    "user": ["email", "full_name", "id", "username"]
}
const values = {
    "register success": ["User registered successfully", 1],
    "register duplicate": ["Cannot register user: the username 'denis' already exists"],
    "register missing username": ["The username must be at least " + MIN_USERNAME_LENGTH + " characters long"],
    "register missing email": ["Email required"],
    "register missing full_name": ["The full name must be at least " + MIN_FULL_NAME_LENGTH + " characters long"],
    "register missing password": ["The password must be at least " + MIN_PASSWORD_LENGTH + " characters long"],
    "login invalid": ["Wrong username or password"],
    "login missing username or password": ["Missing username or password"],
    "who_am_i missing auth header": ["Missing Authorization Header"],
    "who_am_i invalid signature": ["Signature verification failed"],
    "who_am_i token expired": ["Token has expired"],
    "who_am_i invalid token": ["Not enough segments"],
    "who_am_i valid": ["denis@example.com", "Denis 123", 1, "denis"],
    "fresh_only valid fresh token": ["the given token is fresh"],
    "fresh_only valid not fresh token": ["Fresh token required"],
    "refresh expired token": ["Token has expired"],
    "refresh non-refresh token": ["Only refresh tokens are allowed"],
    "refresh expired non-refresh token": ["Token has expired"]
}

client.test("Request executed successfully", function () {
    const expected = request.variables.get("statusCode");
    client.assert(response.status === parseInt(expected),
        "Response status is " + response.status + " instead of " + expected);
});

client.test("Response content-type is json", function () {
    const type = response.contentType.mimeType;
    client.assert(type === "application/json", "Expected 'application/json' but received '" + type + "'");
});


const test_keys = request.variables.get("keys")
const test_values = request.variables.get("values")
client.test(test_keys + " options exist and have correct values", function () {
    // for (let i = 0; i < keys[test_keys].length; i++) {
    //     let key = keys[test_keys][i]
    // const value = values[test_values][i]
    // client.assert(response.body.hasOwnProperty(key), "Cannot find '" + key + "' option in response " + response.body[key]);
    // }
    for (let i = 0; i < keys[test_keys].length; i++) {
        let key = keys[test_keys][i]
        let value = values[test_values][i]
        let expected = JSON.stringify(value)
        let actual = JSON.stringify(response.body[key])
        client.assert(response.body.hasOwnProperty(key), "Cannot find '" + key + "' option in response " + response.body[key]);
        client.assert(actual === expected, "Values for " + key + " don't match: expected " + expected + " got " + actual)
    }
});

