class HttpError extends Error {
    constructor(status, ...params) {
        super(...params);

        if (Error.captureStackTrace)
            Error.captureStackTrace(this, HttpError);

        this.status = status;
    }
}

HttpError.BadRequest = new HttpError(400, '잘못된 요청');
HttpError.Unauthorized = new HttpError(401, '로그인을 해주세요');
HttpError.Forbidden = new HttpError(403, '접근할 수 있는 권한이 없습니다');
HttpError.NotFound = new HttpError(404, '해당 리소스를 찾을 수 없습니다');

module.exports = HttpError;