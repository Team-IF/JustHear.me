const express = require('express');
const asynchandler = require('../utils/asynchandler');

const auther = require('../middleware/auth');
const HttpError = require('../models/httperror');
const User = require('../models/user');

const router = express.Router();

router.use(express.json());

// UUID 로 프로필 찾기
router.get('/view/:id', asynchandler(async (req, res) => {
    if (!req.params.id)
        throw HttpError.BadRequest;

    let user = await User.findById(req.params.id).exec();
    if (user)
        res.send(user.toJSON()); // 프로필 공개 수준 설정 잇으면 좋을듯
    else
        throw HttpError.NotFound;
}));

// 프로필 수정
router.put('/edit/:id', asynchandler(auther), asynchandler(async (req, res) => {
    if (!req.session || !req.session.checkValidation())
        throw HttpError.Unauthorized;

    if (req.session.uuid !== req.params.id)
        throw HttpError.Forbidden;

    const user = await User.findById(req.session.uuid).exec();

    if (!user)
        throw HttpError.NotFound;

    await user.updateOne(req.body, { omitUndefined: true });
    res.send(user.toJSON());
}));

router.delete('/delete/:id', (req, res) => {

});

router.post('/registry', asynchandler(async (req, res) => {
    // 이미 등록된 이메일인지 확인
    const checkuser = await User.findByEmail(req.body.email).exec();
    if (Array.isArray(checkuser) && checkuser.length > 0)
        throw new HttpError(400, '이미 존재하는 이메일');

    const user = new User(req.body);
    await user.savePassword(req.body.pass);
    await user.save();

    res.status(204).send('');
}));

module.exports = router;
