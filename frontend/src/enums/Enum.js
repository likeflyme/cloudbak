export const createEnum = (definition) => {
    const enum_data = {}
    const value_enum = {}
    for (const name of Object.keys(definition)) {
        const [value, desc] = definition[name]
        const data = {value, desc};
        enum_data[name] = data;
        value_enum[value] = data;
    }
    return {
        ...enum_data,
        ...value_enum,
        fromValue(value) {
            return value_enum[value];
        },
        keys() {
            return Object.keys(enum_data)
        }
    }
}