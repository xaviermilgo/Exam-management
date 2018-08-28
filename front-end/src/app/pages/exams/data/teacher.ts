import {Role} from "./role";
export class Teacher {
    constructor(
        public name:string,
        public phoneNumber:string,
        public roles:Role[]
    ){

    }
}
