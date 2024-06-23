import Mock from "mockjs";
import { userUrl } from '@/service/api'
 
export const registerResult = Mock.mock(import.meta.env.VITE_API_URL+userUrl.register, "post", {
    value: {
        message: "User registered successfully",
        userId: 123
    },
    status: 201
});

export const loginResult = Mock.mock(import.meta.env.VITE_API_URL+userUrl.login, "post", {
    value: {
        token: "jwt_token",
        userId: 123, 
        role: "student"
    },
    status: 200    
});