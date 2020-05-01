const express = require("express");

const moment = require('moment');
const bcrypt = require('bcrypt');
const HttpError = require("../models/httperror");
const Session = require('../models/session');
const uuid = require("../utils/uuid");
const asynchandler = require("../utils/asynchandler");
const auther = require("../middleware/auth");

const router = express.Router();

router.use(express.json());

router.post('/login', asynchandler(async (req, res) => {
    if (!req.body.email || !req.body.pass)
        throw new HttpError(400, "이메일과 비밀번호를 입력해 주세요.");

    const db = req.app.locals.db;
    const userdata = db.collection('user_data');
    const user = await userdata.findOne({ email: userdata.email }, { projection: { uuid: 1, pass: 1 } });

    if (!user || !bcrypt.compare(req.body.pass, user.pass))
        throw new HttpError(403, "잘못된 이메일/비밀번호");

    const sessions = db.collection('sessions');
    const session = Session.createNew(user.uuid);
    await sessions.insertOne(session);

    res.send({
        token: session.accessToken,
        uuid: user.uuid
    });
}));

router.post('/refresh', asynchandler(async (req, res) => {

}));

router.get('/invalidate', asynchandler(auther), asynchandler(async (req, res) => {
    if (!req.session)
        throw new HttpError(401, "로그인을 해주세요.");

    const oldtoken = req.session.accessToken;

    const db = req.app.locals.db;
    const sessions = db.collection('sessions');

    await sessions.deleteMany({ accessToken: oldtoken });

    res.status(204).send('');
}));

module.exports = router;
