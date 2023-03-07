const keys = {
    "success": ["success", "data"],
    "error": ["success", "error", "code"],
    "msg": ["msg"]
}
const values = {
    "get_all_contacts": [true, [
        {
            "address": null,
            "contact_id": 1,
            "email": null,
            "name": "Denis",
            "phone": null
        },
        {
            "address": null,
            "contact_id": 2,
            "email": "bob@example.com",
            "name": "Bob",
            "phone": null
        }
    ]],
    "get_contact_1": [true, {
        "address": null,
        "contact_id": 1,
        "email": null,
        "name": "Denis",
        "phone": null
    }],
    "get_all_calls_contact_1": [true, [
        {
            "call_id": 1,
            "datetime": "2023-02-13 16:45:53.917489",
            "phone": "1112223333"
        },
        {
            "call_id": 4,
            "datetime": "2023-02-13 16:53:10.446698",
            "phone": "1112223333"
        }
    ]],
    "post_new_contact_1": [true, {
        "address": null,
        "contact_id": 3,
        "email": null,
        "name": "New Contact",
        "phone": null
    }],
    "post_new_contact_2": [true, {
        "address": "Québec",
        "contact_id": 4,
        "email": "new@example.com",
        "name": "New Contact",
        "phone": "111-222-3333"
    }],
    "error_404": [false, "Not Found", 404],
    "msg_404": ["Not Found"]
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

