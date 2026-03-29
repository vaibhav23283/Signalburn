
export const AuthService = {
    async sendOTP(phoneNumber: string): Promise<boolean> {
        // Simulate API call
        console.log(`Sending OTP to ${phoneNumber}`);
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(true);
            }, 1000);
        });
    },

    async verifyOTP(phoneNumber: string, otp: string): Promise<boolean> {
        // Mock verification: Any 6 digit code starting with 123 is valid for testing
        // Or just '123456'
        return new Promise((resolve) => {
            setTimeout(() => {
                if (otp === '123456') {
                    resolve(true);
                } else {
                    resolve(false);
                }
            }, 1000);
        });
    },

    async logout(): Promise<void> {
        // Clear auth data if any
        // For now just clear profile and contacts if we want to reset
        // In a real app we'd clear the JWT token
    }
};
