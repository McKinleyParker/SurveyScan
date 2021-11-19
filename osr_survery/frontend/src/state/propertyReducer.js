const propertyListReducer = (state=1, action) => {
    switch (action.type) {
        case "add":
            return state + action.payload;
        case "subtract":
            return state - action.payload;
        case "clear":
            return 0;
        case "set":
            return action.payload;
        default:
            return state;
    }
};

export default propertyListReducer