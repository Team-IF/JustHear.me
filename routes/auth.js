const express = require("express");

const moment = require('moment');
const bcrypt = require('bcrypt');
const HttpError = require("../models/httperror");
const Session = require('../models/session');
const User = require("../models/user");
const uuid = require("../utils/uuid");
const asynchandler = require("../utils/asynchandler");
const auther = require("../middleware/auth");

const router = express.Router();

router.use(express.json());

router.post('/login', asynchandler(async (req, res) => {
    if (!req.body.email || !req.body.pass)
        throw new HttpError(400, "이메일과 비밀번호를 입력해 주세요.");

    const user = await User.findById(req.body.email);

    if (!user || !user.comparePassword(req.body.pass))
        throw new HttpError(403, "잘못된 이메일/비밀번호");

    const session = Session.createNew(user._id);
    session.save();

    res.send({
        token: session.accessToken,
        uuid: user.uuid
    });
}));

router.post('/refresh', asynchandler(async (req, res) => {

}));

router.get('/invalidate', asynchandler(auther), asynchandler(async (req, res) => {
    if (!req.session || !req.session.checkValid())
        throw new HttpError(401, "로그인을 해주세요.");

    const oldtoken = req.session.accessToken;
    await Session.deleteMany({ accessToken: oldtoken });

    res.status(204).send('');
}));

module.exports = router;
