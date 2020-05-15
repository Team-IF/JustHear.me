const express = require('express');
const HttpError = require('../models/httperror');
const Session = require('../models/session');
const User = require('../models/user');
const asynchandler = require('../utils/asynchandler');
const auther = require('../middleware/auth');

const router = express.Router();

router.use(express.json());

router.post('/login', asynchandler(async (req, res) => {
    if (!req.body.email || !req.body.pass)
        throw HttpError.Unauthorized;

    const user = await User.findByEmail(req.body.email).exec();

    if (!user || !await user.comparePassword(req.body.pass))
        throw new HttpError(403, '잘못된 이메일, 비밀번호');

    const session = Session.createNew(user._id);
    await session.save();

    res.send({
        token: session.accessToken,
        uuid: user.uuid
    });
}));

router.post('/refresh', asynchandler(async (req, res) => {

}));

router.get('/invalidate', asynchandler(auther), asynchandler(async (req, res) => {
    if (!req.session || !req.session.checkValidation())
        throw HttpError.Unauthorized;

    const oldtoken = req.session.accessToken;
    await Session.deleteMany({ accessToken: oldtoken }).exec();

    res.status(204).send('');
}));

module.exports = router;
