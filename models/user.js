const bcrypt = require('bcrypt');
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const bcryptSaltRounds = 10;

const emailreg = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/;
const phonereg = /[+][0-9]+/;

const userSchema = new Schema({
    username: {
        type: String,
        required: true,
        minlength: 1,
        maxlength: 30
    },
    email: {
        type: String,
        required: true,
        match: emailreg,
        minlength: 3,
        maxlength: 254 // RFC 5321
    },
    phonenumber: {
        type: String,
        match: phonereg,
        maxlength: 15 // 국제표준
    },
    gender: {
        type: String,
        enum: ['M', 'F'] // 중성? 추가필요?
    },
    birthday: Date,
    password: String,
    profileImg: String,
    profileMusic: String,
    createdAt: Date,
    updatedAt: Date
}, {
    timestamps: {
        createdAt: 'createdAt',
        updatedAt: 'updatedAt'
    }
});

userSchema.methods.comparePassword = function (plainPassword) {
    return bcrypt.compare(plainPassword, this.password);
};

userSchema.methods.savePassword = async function (plainPassword) {
    this.password = await bcrypt.hash(plainPassword, bcryptSaltRounds);
};

userSchema.statics.findByEmail = function (email) {
    return this.findOne({ email: email });
};

const User = mongoose.model('User', userSchema);

module.exports = User;