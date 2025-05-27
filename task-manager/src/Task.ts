// Define interfaces for Task data
export interface TaskData {
    title: string;
    completed?: boolean;
    createdAt?: Date | string;
    description?: string;
    priority: Priority;
    dueDate?: string;
    category: string; 
   }
export type Priority = 'low' | 'medium' | 'high';
export type Category = 'work' | 'personal' | 'general' | 'shopping' | 'other';
   // Task class with TypeScript types
export default class Task {
    title: string;
    completed: boolean;
    createdAt: Date;
    description: string;
    priority: Priority;
    dueDate?: Date;
    category: Category;
   
    constructor(title: string, description: string = '', priority: Priority = 'medium', dueDate?: string, category: Category = 'general') {
    this.dueDate = dueDate ? new Date(dueDate) : undefined;    
    this.priority = priority;
    this.title = title;
    this.description = description;
    this.completed = false;
    this.createdAt = new Date();
    this.category = category;
    }
    // Add method to check if task is overdue
    isOverdue(): boolean {
    if (!this.dueDate || this.completed) return false;
    return this.dueDate < new Date();
    }
   
   
    // Method to toggle completion status
    toggleComplete() {
    this.completed = !this.completed;
    return this;
    }
   
  // Static method with parameter and return type
 static fromObject(obj: TaskData): Task {
    const task = new Task(obj.title, obj.description || '', obj.priority || 'medium', );
   
    if (obj.completed !== undefined) {
    task.completed = obj.completed;
    }
   
    if (obj.createdAt) {
    task.createdAt = new Date(obj.createdAt);
    }
   
    return task;
}
   }
   