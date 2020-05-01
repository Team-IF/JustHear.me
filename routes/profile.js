const express = require("express");
const bcrypt = require("bcrypt");
const uuid = require("../utils/uuid");
const asynchandler = require("../utils/asynchandler");

const auther = require("../middleware/auth");
const HttpError = require("../models/httperror");
const User = require("../models/user");

const router = express.Router();

const bcryptSaltRounds = 10;

router.use(express.json());

// UUID 로 프로필 찾기
router.get('/:id', asynchandler(async (req, res) => {
    if (!req.body.uuid)
        throw new HttpError(400);

    const userdata = req.app.locals.db.collection('user_data');
    res.send(await userdata.findOne({ uuid: req.params.id }, { projection: { pass: 0 } })); // 프로필 공개 수준 설정 잇으면 좋을듯
}));

// 프로필 수정
router.put('/:id', asynchandler(auther), asynchandler(async (req, res) => {
    if (!req.session)
        throw new HttpError(401, '로그인을 해주세요.');

    if (req.session.uuid !== req.params.id)
        throw new HttpError(403, '자신의 프로필만 수정할 수 있습니다.');

    const userdata = req.app.locals.db.collection('user_data');
    const user = await userdata.findOne({ uuid: req.params.id }, { projection: { pass: 0 } });

    if (!user)
        throw new HttpError(404, '해당 프로필을 찾을 수 없습니다.');

    const newUser = new User.Builder()
        .fromObj(user)
        .fromObj(req.body)
        .build();

    await userdata.findOneAndUpdate({ uuid: req.params.id }, newUser);

    res.send(newUser);
}));

router.delete('/:id', (req, res) => {

});

router.post('/registry', asynchandler(async (req, res) => {
    const db = req.app.locals.db;
    const userdata = db.collection('user_data');

    // 이미 등록된 이메일인지 확인
    const checkuser = userdata.findOne({ email: req.body.email });
    if (checkuser)
        throw new HttpError(400, "이미 존재하는 이메일");

    // 비밀번호 해싱
    req.body.pass = await bcrypt.hash(req.body.pass, bcryptSaltRounds);

    // 유저 객체 생성
    const user = new User.Builder()
        .fromObj(req.body)
        .build();

    // 디비 기록
    await userdata.insertOne(user);

    res.status(204).send('');
}));

module.exports = router;
