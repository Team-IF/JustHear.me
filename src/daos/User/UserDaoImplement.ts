import { User } from '@entities/UserImplement';


export interface UserDao {
    getOne: (email: string) => Promise<User | null>;
    getAll: () => Promise<User[]>;
    add: (user: User) => Promise<void>;
    update: (user: User) => Promise<void>;
    delete: (id: number) => Promise<void>;
}

class UserDaoImplement implements UserDao {


    /**
     * @param email
     */
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    public async getOne(email: string): Promise<User | null> {
        // TODO
        return [] as any;
    }


    /**
     *
     */
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    public async getAll(): Promise<User[]> {
        // TODO
        return [] as any;
    }


    /**
     *
     * @param user
     */
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    public async add(user: User): Promise<void> {
        // TODO
        return {} as any;
    }


    /**
     *
     * @param user
     */
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    public async update(user: User): Promise<void> {
        // TODO
        return {} as any;
    }


    /**
     *
     * @param id
     */
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    public async delete(id: number): Promise<void> {
        // TODO
        return {} as any;
    }
}

export default UserDaoImplement;
