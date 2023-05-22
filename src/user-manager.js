import {syncToLocalStorage as syncState, systemState} from "@/system";
import axios from "axios";

let CryptoJS = require("crypto-js")

export class VirtualUserDatabase {
    static validSessionTime = 60000

    static users = [
        {
            name: "User1",
            id: "user1",
            passwordHash: "6b908b785fdba05a6446347dae08d8c5",  //User1
            permissionGroup: "user",
            permission: "*****"
        },
        {
            name: "Admin",
            id: "admin",
            passwordHash: "21232f297a57a5a743894a0e4a801fc3",
            permissionGroup: "admin",
            permission: "*****"
        }
    ]

    static sessions = [
        {
            sessionId: "session_example",
            sessionDate: 0,
            userId: "user1"
        }
    ]

    static syncToLocalStorage() {
        this.clearOutDatedSession()

        localStorage.setItem("virtual-users", JSON.stringify(this.users))
        localStorage.setItem("virtual-sessions", JSON.stringify(this.sessions))
    }

    static initDatabase() {
        let vu = localStorage.getItem("virtual-users")
        let vs = localStorage.getItem("virtual-sessions")
        if (vu === null || vu === undefined) {
            this.syncToLocalStorage()
        } else {
            this.users = JSON.parse(vu)
        }

        if (vs === null || vs === undefined) {
            this.syncToLocalStorage()
        } else {
            this.sessions = JSON.parse(vs)
        }
    }

    static getUserById(id) {
        for (let user of this.users) {
            if (user.id === id) {
                return user
            }
        }
        return undefined
    }

    static getUserBySession(sessionId, checkDate = true) {
        for (let session of this.sessions){
            if (session.sessionId === sessionId) {
                if (!checkDate || session.sessionDate > Date.now()) {
                    return this.getUserById(session.userId)
                }
            }
        }

        return undefined
    }

    static getUserSession(sessionId){
        for (let session of this.sessions){
            if (session.sessionId === sessionId) {
                return session
            }
        }
        return undefined
    }

    static clearOutDatedSession(update = false){
        this.sessions = this.sessions.filter(session => session.sessionDate > Date.now())
        if(update) this.syncToLocalStorage()
    }

    static addUserSession(userId) {
        let session = generateSession(this.containsSession)
        console.log(this.sessions)
        this.sessions.push({
            sessionId: session,
            sessionDate: Date.now() + this.validSessionTime,
            userId: userId
        })
        VirtualUserDatabase.syncToLocalStorage()
        return session
    }

    static updateUserSession(sessionId){
        for (let session of this.sessions){
            if (session.sessionId === sessionId) {
                session.sessionId = generateSession(this.containsSession)
                session.sessionDate = Date.now() + this.validSessionTime
                this.syncToLocalStorage()
                return session
            }
        }
        return undefined
    }

    static removeUserSession(sessionId) {
        console.log('尝试删除session: ' + sessionId)
        for (let i = 0; i < this.sessions.length; i++) {
            if (this.sessions[i].sessionId === sessionId) {
                this.sessions.splice(i, 1)
                this.syncToLocalStorage()
                console.log('已删除session: ' + sessionId)
                return true
            }
        }
        return false
    }

    static verifySession(userId, sessionId){
        let session = this.getUserSession(sessionId)
        if(session === undefined){
            return false
        }
        if(session.userId !== userId){
            return false
        }
        if(session.sessionDate < Date.now()){
            return false
        }
        return true
    }

    static verify(id, hash) {
        let user = this.getUserById(id)
        if (user === undefined) {
            return false
        }
        return user.passwordHash === hash
    }

    static login(id, hash) {
        let user = this.getUserById(id)
        if (user === undefined) {
            // return buildResponsePacket(false, "用户不存在")
            return buildResponsePacket(false, "用户名或密码错误")
        }
        if (user.passwordHash === hash) {
            this.removeUserSession(systemState.currentSession)
            let session = this.addUserSession(user.id)
            return buildResponsePacket(true, `登录成功，欢迎${user.name}`, session)
        }
        // return buildResponsePacket(false, "密码错误")
        return buildResponsePacket(false, "用户名或密码错误")
    }

    static loginBySession(sessionId) {
        let user = this.getUserBySession(sessionId, false)
        if (user !== undefined) {
            let session = this.getUserSession(sessionId)
            if(session.sessionDate < Date.now()){
                this.removeUserSession(sessionId)
                return buildResponsePacket(false, "会话过期，请重新登录")
            }
            session = this.updateUserSession(sessionId)
            return buildResponsePacket(true, `登录成功，欢迎${user.name}`, session.sessionId)
        }
        return buildResponsePacket(false, "会话过期，请重新登录")
    }

    static containsSession(sessionId) {
        for (let session of VirtualUserDatabase.sessions) {
            if (session.sessionId === sessionId) {
                return true
            }
        }
        return false
    }

    static logout(sessionId) {
        this.removeUserSession(sessionId)
    }

    static register(name, id, hash, permissionGroup, permission) {
        let user = this.getUserById(id)
        if (user !== undefined) {
            //不允许重复的id
            return buildResponsePacket(false, "用户已存在")
        }
        this.users.push({
            name: name,
            id: id,
            passwordHash: hash,
            permissionGroup: permissionGroup,
            permission: permission
        })
        return buildResponsePacket(true, "注册成功")
    }

    static updateUserInfo(userId, sessionId, infoKey, infoValue){
        let user = this.getUserById(userId)
        if(user === undefined){
            return buildResponsePacket(false, "用户不存在")
        }
        if(!this.verifySession(userId, sessionId)){
            return buildResponsePacket(false, "会话过期，请重新登录")
        }
        if(infoKey === "passwordHash"){
            return buildResponsePacket(false, "不允许修改密码，请使用专用接口")
        }
        user[infoKey] = infoValue
        return buildResponsePacket(true, "修改成功")
    }

    static updatePassword(id, session, hash) {
        let user = this.getUserById(id)
        if (user === undefined) {
            return buildResponsePacket(false, "用户不存在")
        }
        if (!this.verifySession(id, session)) {
            return buildResponsePacket(false, "会话过期，请重新登录")
        }
        user.passwordHash = hash
        return buildResponsePacket(true, "密码修改成功")
    }
}

function md5_32(str) {
    return CryptoJS.MD5(str).toString()
}

function generateSession(duplicateCheck = (() => false)){
    //使用uuid v4生成不重复的session
    let retry = true
    let session = ""
    while (retry){
        let uuid = require("uuid")
        session = uuid.v4()
        retry = duplicateCheck(session)
    }

    console.log(`生成新的session: ${session}`)
    return session
}

function buildResponsePacket(success, message, data = undefined){
    return {
        success: success,
        message: message,
        data: data
    }
}

// eslint-disable-next-line no-unused-vars
export function requestLogin(id, hash) {
    if(systemState.globalSettings.virtualMode){
        return new Promise((resolve) => {
            let response = VirtualUserDatabase.login(id, hash)
            if (response.success) {
                setCurrentUser(response.data)
            }
            resolve(response)
        })
    }else {
        //TODO: 从后端数据库中获取用户信息，验证用户身份并更新session与currentUser
        axios.defaults.baseURL = systemState.globalSettings.backendUrl
        let request = axios.post("/request/login", {
            id: id,
            hash: hash
        })
        return new Promise((resolve) => {
            request.then(response => {
                if(response.data.success){
                    setCurrentUser(response.data.data)
                }
                resolve(response.data)
            }).catch(error => {
                resolve({
                    success: false,
                    message: error.message,
                    data: error
                })
            })
        })
    }
}

// eslint-disable-next-line no-unused-vars
export function requestLoginBySession(sessionId){
    //TODO: 从后端数据库中获取session，验证合法性并返回登录结果
    if (systemState.globalSettings.virtualMode) {
        return new Promise((resolve) => {
            let response = VirtualUserDatabase.loginBySession(sessionId)
            if (response.success) {
                setCurrentUser(response.data)
            }
            resolve(response)
        })
    }else{
        axios.defaults.baseURL = systemState.globalSettings.backendUrl
        let request = axios.post("/request/loginBySession", {
            sessionId: sessionId
        })
        return new Promise((resolve) => {
            request.then(response => {
                if(response.data.success){
                    setCurrentUser(response.data.data)
                }
                resolve(response.data)
            }).catch(error => {
                resolve({
                    success: false,
                    message: error.message,
                    data: error
                })
            })
        })
    }
}

export function requestLogout(sessionId){
    if(systemState.globalSettings.virtualMode){
        return new Promise(resolve => {
            VirtualUserDatabase.logout(sessionId)
            resolve(buildResponsePacket(true, "登出成功"))
        })
    }else{
        axios.defaults.baseURL = systemState.globalSettings.backendUrl
        let request = axios.post("/request/logout", {
            sessionId: sessionId
        })
        return new Promise((resolve) => {
            request.then(response => {
                resolve(response.data)
            }).catch(error => {
                resolve({
                    success: false,
                    message: error.message,
                    data: error
                })
            })
        })
    }
}

export function requestRegister(id, hash){
    if(systemState.globalSettings.virtualMode){
        return new Promise(resolve => {
            resolve(VirtualUserDatabase.register(id, id, hash, "restrict", "*****"))
        })
    }else{
        axios.defaults.baseURL = systemState.globalSettings.backendUrl
        let request = axios.post("/request/register", {
            id: id,
            hash: hash
        })
        return new Promise((resolve) => {
            request.then(response => {
                resolve(response.data)
            }).catch(error => {
                resolve({
                    success: false,
                    message: error.message,
                    data: error
                })
            })
        })
    }
}

export function hashPassword(password) {
    return md5_32(password)
}

function setCurrentUser(sessionId){
    systemState.currentSession = sessionId
    syncState()
}

if(systemState.globalSettings.virtualMode){
    VirtualUserDatabase.initDatabase()
    console.log("虚拟用户数据库初始化完成")
}