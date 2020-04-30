const moment = require('moment');
const uuid = require('../utils/uuid');

class Session {
    constructor(uuid, token, expireDate) {
        this.uuid = uuid;
        this.accessToken = token;

        if (expireDate instanceof moment)
            this.expireDate = expireDate;
        else
            this.expireDate = moment(expireDate);
    }

    checkValid() {
        return moment().isBefore(this.expireDate);
    }

    static createNew(uuid) {
        const uuid = uuid;
        const token = uuid();
        const exp = moment().add(14, "days");

        return new Session(uuid, token, exp);
    }
}

module.exports = Session;