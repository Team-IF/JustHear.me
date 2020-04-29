const express = require("express");
const uuid = require("../utils/uuid");
const user = require("../models/user");
const router = express.Router();

router.get('/:id', (req, res) => {

});

router.put('/:id', (req, res) => {

});

router.delete('/:id', (req, res) => {

});

router.post('/registry', (req, res) => {

    // TODO: 이메일 이미 등록됫는지 확인

    let user = new user.UserBuilder()
        .setUuid(uuid())
        .setBirthday(req.body.birthday)
        .setEmail(req.body.email)
        .setGender(req.body.gender)
        .setPhoneNumber(req.body.phonenumber)
        .setProfileImg(req.body.profileImg)
        .setProfileMusic(req.body.profileMusic)
        .setUsername(req.body.username)
        .encPassword(req.body.pass)
        .build();

    // TODO: db 등록

    res.status(204).send('');
});

module.exports = router;
