const moment = require('moment');
const mongoose = require('mongoose');
const Schema = mongoose.Schema;
const uuid = require('../utils/uuid');

const sessionSchema = new Schema({
    userId: {
        type: String,
        required: true
    },
    accessToken: {
        type: String,
        required: true
    },
    expireDate: {
        type: Date,
        required: true
    }
});

sessionSchema.methods.checkValidation = function () {
    return moment().isBefore(this.expireDate);
};

sessionSchema.statics.findByToken = function (token) {
    return this.findOne({ accessToken: token });
};

sessionSchema.statics.createNew = function (userid) {
    const token = uuid();
    const exp = moment().add(14, 'days').toDate();

    return new Session({
        userId: userid,
        accessToken: token,
        expireDate: exp
    });
};

const Session = mongoose.model('Session', sessionSchema);

module.exports = Session;