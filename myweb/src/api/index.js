import http from '../utils/request'

export const getFormulation = (params) => {
    return http.get('/formulation/formulation_list', params) //返回配方列表
}
export const addFormulation = (data) => {
    return http.post('/formulation/formulation_add/',data) //新增配方
}
export const editFormulation = (data) => {
    return http.post(`/formulation/formulation_update/${data.formulation_id}/`,data) //编辑配方
}
export const delFormulation = (data) => {
    return http.post(`/formulation/formulation_del/${data.id}/`,data) //删除配方
}
export const getData = () => {
    // 返回一个promise对象
    return http.get('/formulation/formulation_list')
}
