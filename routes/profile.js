const express = require("express");
const bcrypt = require("bcrypt");
const uuid = require("../utils/uuid");


const HttpError = require("../models/httperror").HttpError;
const User = require("../models/user").User;
const UserBuilder = require("../models/user").UserBuilder;

const router = express.Router();

const bcryptSaltRounds = 10;

router.use(express.json());

// UUID 로 프로필 찾기
router.get('/:id', (req, res) => {
    if (!req.body.uuid)
        throw new HttpError(400);

    const userdata = req.app.locals.db.collection('user_data');
    return userdata.findOne({ uuid: req.params.id }, { projection: { pass: 0 } }); // 프로필 공개 수준 설정 잇으면 좋을듯
});

// 프로필 수정
router.put('/:id', auther, (req, res) => {

});

router.delete('/:id', (req, res) => {

});

router.post('/registry', async (req, res) => {
    const db = req.app.locals.db;
    const userdata = db.collection('user_data');

    // 이미 등록된 이메일인지 확인
    const checkuser = userdata.findOne({ email: req.body.email });
    if (checkuser)
        throw new HttpError(400, "이미 존재하는 이메일");

    // 비밀번호 해싱
    req.body.pass = await bcrypt.hash(req.body.pass, bcryptSaltRounds);

    // 유저 객체 생성
    const user = new UserBuilder().fromObj(req.body);

    // 디비 기록
    await userdata.insertOne(user);

    res.status(204).send('');
});

module.exports = router;
