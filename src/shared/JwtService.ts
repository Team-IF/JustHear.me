import randomString from 'randomstring';
import jsonwebtoken, { VerifyErrors } from 'jsonwebtoken';
import { cookieProps } from '@shared/constants';


interface ClientData {
    id: number;
    role: number;
}

export class JwtService {

    private readonly secret: string;
    private readonly options: object;
    private readonly VALIDATION_ERROR = 'JSON-web-token validation failed.';


    constructor() {
        this.secret = (process.env.JWT_SECRET || randomString.generate(100));
        this.options = {expiresIn: cookieProps.options.maxAge.toString()};
    }


    /**
     * Encrypt data and return jwt.
     *
     * @param data
     */
    public getJwt(data: ClientData): Promise<string> {
        return new Promise((resolve, reject) => {
            jsonwebtoken.sign(data, this.secret, this.options, (err, token) => {
                if (err) reject(err); else resolve(token);
            });
        });
    }


    /**
     * Decrypt JWT and extract client data.
     *
     * @param jwt
     */
    public decodeJwt(jwt: string): Promise<ClientData> {
        return new Promise((res, rej) => {
            jsonwebtoken.verify(jwt, this.secret, (err: VerifyErrors | null, decoded: object | undefined) => {
                return err ? rej(this.VALIDATION_ERROR) : res(decoded as ClientData);
            });
        });
    }
}
