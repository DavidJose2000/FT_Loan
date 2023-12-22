$.validator.addMethod(
    "regex",
    function (value, element, regexp) {
        var re = new RegExp(regexp);
        return this.optional(element) || re.test(value);
    },
    "Please check your input."
);

$.validator.addMethod(
    "phone_num",
    function (value, element) {
        var re = new RegExp('^([0-9]{10,15})$');
        return this.optional(element) || re.test(value);
    },
    "Please enter valid phone number."
);

$.validator.addMethod(
    "alpha_only",
    function (value, element) {
        var re = new RegExp('^[A-Za-z ]+$');
        return this.optional(element) || re.test(value);
    },
    "Only alphabets are accepted."
);

$.validator.addMethod(
    "alphanum_only",
    function (value, element) {
        var re = new RegExp('^[0-9a-zA-Z]+$');
        return this.optional(element) || re.test(value);
    },
    "Only alphabets and numbers are accepted."
);

$.validator.addMethod(
    "num_only",
    function (value, element) {
        var re = new RegExp('^[0-9]+$');
        return this.optional(element) || re.test(value);
    },
    "Only numbers are accepted."
);