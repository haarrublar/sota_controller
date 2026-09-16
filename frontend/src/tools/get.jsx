import axios from "axios";

const BASE_URL = 'http://127.0.0.1:8000/api';
const BUTTONS_CACHE = `${BASE_URL}/controller-events/recent/`;


export const get_button_cache = async () => {
    try {
        const response = await axios.get(
            BUTTONS_CACHE, {
                withCredentials: false
            }
        );
        return response.data
    } catch (error) {
        return error 
    }
}



