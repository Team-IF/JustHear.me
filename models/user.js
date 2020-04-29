const moment = require("moment");

const emailreg = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/;
const phonereg = /[+][0-9]+/;

class User {
    constructor(uuid, username, email, password, phonenumber, birthday, gender, profileimg, profilemusic) {
        this.uuid = uuid;
        this.username = username;
        this.email = email;
        this.password = password;
        this.phonenumber = phonenumber;
        this.birthday = birthday;
        this.gender = gender;
        this.profileimg = profileimg;
        this.profilemusic = profilemusic;
    }

    // 특정 프로퍼티만 반환
    filter(propertyNames) {
        let obj = {};
        Object.keys(this)
            .filter(x => propertyNames.includes(x))
            .forEach(x => obj[x] = this[x]);

        return obj;
    }
}

class UserBuilder { // builder pattern of User class
    setUuid(uuid) {
        this.uuid = uuid;
        return this;
    }

    setUsername(username) {
        this.username = username;
        return this;
    }

    setEmail(email) {
        if (email.match(emailreg))
            this.email = email;
        else
            throw new Error("Invalid email format");
        return this;
    }

    setEncryptedPassword(password) {
        this.password = password;
        return this;
    }

    setPhoneNumber(number) {
        if (!number)
            this.number = undefined;
        else if (number.match(phonereg))
            this.phonenumber = number;
        else
            throw new Error("Invalid phone number format");
        return this;
    }

    setBirthday(bd) {
        if (!bd)
            this.bd = undefined;
        else if (bd instanceof moment)
            this.birthday = bd.format('YYYY-MM-DD');
        else if (typeof (bd) === "string")
            this.birthday = bd;
        else
            throw new Error("Unexpected Type of bd");

        return this;
    }

    setGender(g) {
        if (!g)
            this.gender = undefined;
        else if (typeof (g) === "string")
            this.gender = g;
        else
            throw new Error("Unexpected Type of g");

        return this;
    }

    setProfileImg(p) {
        this.profileimg = p;
        return this;
    }

    setProfileMusic(p) {
        this.profilemusic = p;
        return this;
    }

    build() {
        return new User(
            this.uuid,
            this.username,
            this.email,
            this.password,
            this.phonenumber,
            this.birthday,
            this.gender,
            this.profileimg,
            this.profilemusic,
        );
    }
}

module.exports = {
    User: User,
    UserBuilder: UserBuilder
};