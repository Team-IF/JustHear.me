const express = require("express");
const jwt = require('jsonwebtoken');
const router = express.Router();
let db;

function createToken() {
    return new Promise((resolve, reject) => {

    });
}

router.use(express.json());

router.post('/login', (req, res) => {
    if (!req.body.email || !req.body.pass)
        throw new HttpError(400, "이메일과 비밀번호를 입력해 주세요.");

    let user = User.fromEmail(req.body.email);
    if (!user)
        throw new HttpError(403, "잘못된 이메일/비밀번호");

    let pw = encPw(req.body.pass);
    if (user.pass !== pw)
        throw new HttpError(403, "잘못된 이메일/비밀번호");
});



module.exports = function (s) {
    db = s;
    return router;
};
