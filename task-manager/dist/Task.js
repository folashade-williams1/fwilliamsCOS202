// Task class with TypeScript types
export default class Task {
    constructor(title, description = '', priority = 'medium', dueDate, category = 'general') {
        this.dueDate = dueDate ? new Date(dueDate) : undefined;
        this.priority = priority;
        this.title = title;
        this.description = description;
        this.completed = false;
        this.createdAt = new Date();
        this.category = category;
    }
    // Add method to check if task is overdue
    isOverdue() {
        if (!this.dueDate || this.completed)
            return false;
        return this.dueDate < new Date();
    }
    // Method to toggle completion status
    toggleComplete() {
        this.completed = !this.completed;
        return this;
    }
    // Static method with parameter and return type
    static fromObject(obj) {
        const task = new Task(obj.title, obj.description || '', obj.priority || 'medium');
        if (obj.completed !== undefined) {
            task.completed = obj.completed;
        }
        if (obj.createdAt) {
            task.createdAt = new Date(obj.createdAt);
        }
        return task;
    }
}
