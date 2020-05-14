const express = require("express");
const uuid = require("../utils/uuid");
const asynchandler = require("../utils/asynchandler");

const auther = require("../middleware/auth");
const HttpError = require("../models/httperror");
const User = require("../models/user");

const router = express.Router();

router.use(express.json());

// UUID 로 프로필 찾기
router.get('/:id', asynchandler(async (req, res) => {
    if (!req.body.uuid)
        throw new HttpError(400);

    let user = await User.findById(req.body.uuid);
    res.send(user.toJSON()); // 프로필 공개 수준 설정 잇으면 좋을듯
}));

// 프로필 수정
router.put('/:id', asynchandler(auther), asynchandler(async (req, res) => {
    if (!req.session || !req.session.checkValidation())
        throw new HttpError(401, '로그인을 해주세요.');

    if (req.session.uuid !== req.params.id)
        throw new HttpError(403, '자신의 프로필만 수정할 수 있습니다.');

    const user = await User.findById(req.session.uuid);

    if (!user)
        throw new HttpError(404, '해당 프로필을 찾을 수 없습니다.');

    await user.updateOne(req.body, { omitUndefined: true });
    res.send(user.toJSON());
}));

router.delete('/:id', (req, res) => {

});

router.post('/registry', asynchandler(async (req, res) => {
    // 이미 등록된 이메일인지 확인
    const checkuser = await User.findByEmail(req.body.email);
    if (checkuser)
        throw new HttpError(400, "이미 존재하는 이메일");

    const user = new User(req.body);
    await user.savePassword(req.body.pass);
    await user.save();

    res.status(204).send('');
}));

module.exports = router;
