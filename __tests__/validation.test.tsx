import { fireEvent, render } from '@testing-library/react-native';
import React from 'react';
import { Alert } from 'react-native';
import EmergencyContacts from '../app/setup/contacts';
import ProfileSetup from '../app/setup/profile';

jest.mock('expo-router', () => ({
    useRouter: () => ({ push: jest.fn(), back: jest.fn() }),
}));
jest.mock('react-i18next', () => ({
    useTranslation: () => ({ t: (key: string) => key }),
}));
jest.spyOn(Alert, 'alert');

describe('Validation Logic', () => {
    it('prevents profile save if name is missing', async () => {
        const { getByText } = render(<ProfileSetup />);
        // useTranslation mock returns the key name
        const continueButton = getByText('save_profile');

        fireEvent.press(continueButton);
        expect(Alert.alert).toHaveBeenCalledWith('error', 'name_required');
    });

    it('prevents contact save if phone is too short', async () => {
        const { getByText, getByPlaceholderText } = render(<EmergencyContacts />);
        // This one is hardcoded in contacts.tsx
        const addBtn = getByText('+ Add Contact');
        fireEvent.press(addBtn);

        const nameInput = getByPlaceholderText('e.g., Raj Kumar');
        const relationInput = getByPlaceholderText('e.g., Son / Daughter / Doctor');
        const phoneInput = getByPlaceholderText('Phone number');
        const saveBtn = getByText('Save');

        fireEvent.changeText(nameInput, 'Test');
        fireEvent.changeText(relationInput, 'Family');
        fireEvent.changeText(phoneInput, '123'); // Too short
        fireEvent.press(saveBtn);

        expect(Alert.alert).toHaveBeenCalledWith('Invalid phone', 'Please enter a valid phone number.');
    });
});
