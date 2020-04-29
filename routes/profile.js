const express = require("express");
const bcrypt = require("bcrypt");
const uuid = require("../utils/uuid");
const User = require("../models/user").User;
const UserBuilder = require("../models/user").UserBuilder;
const router = express.Router();

const bcryptSaltRounds = 10;

router.use(express.json());

router.get('/:id', (req, res) => {

});

router.put('/:id', (req, res) => {

});

router.delete('/:id', (req, res) => {

});

router.post('/registry', async (req, res) => {

    // TODO: 이메일 이미 등록됫는지 확인

    let encPw = await bcrypt.hash(req.body.pass, bcryptSaltRounds);

    let user = new UserBuilder()
        .setUuid(uuid())
        .setBirthday(req.body.birthday)
        .setEmail(req.body.email)
        .setGender(req.body.gender)
        .setPhoneNumber(req.body.phonenumber)
        .setProfileImg(req.body.profileImg)
        .setProfileMusic(req.body.profileMusic)
        .setUsername(req.body.username)
        .setEncryptedPassword(encPw)
        .build();

    console.log(user);

    // TODO: db 등록

    res.status(204).send('');
});

module.exports = router;
