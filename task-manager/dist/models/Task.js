// Using nanoid with TypeScript
import { nanoid } from 'nanoid';
export default class Task {
    // Constructor with typed parameters and default values
    constructor(title, description = '', dueDate = null) {
        this.id = nanoid(8);
        this.title = title;
        this.description = description;
        this.dueDate = dueDate;
        this.completed = false;
        this.createdAt = new Date();
    }
    // Method with return type
    toggleComplete() {
        this.completed = !this.completed;
        return this;
    }
    // Static method with parameter and return types
    static fromObject(obj) {
        const task = new Task(obj.title, obj.description || '', obj.dueDate || null);
        if (obj.id)
            task.id = obj.id;
        if (obj.completed !== undefined)
            task.completed = obj.completed;
        if (obj.createdAt)
            task.createdAt = new Date(obj.createdAt);
        return task;
    }
    // Convert to plain object
    toObject() {
        return {
            id: this.id,
            title: this.title,
            description: this.description,
            dueDate: this.dueDate,
            completed: this.completed,
            createdAt: this.createdAt
        };
    }
}
