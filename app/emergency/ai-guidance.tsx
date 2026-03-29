import { rf } from '@/constants/responsive';
import { COLORS, RADIUS, SPACING } from '@/constants/theme';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import * as Speech from 'expo-speech';
import { useEffect, useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { SafeAreaView, ScrollView, StatusBar, Text, TouchableOpacity, View } from 'react-native';

export default function AIGuidance() {
    const router = useRouter();
    const { t, i18n } = useTranslation();
    const [currentStep, setCurrentStep] = useState(0);

    // Dynamic steps based on current language
    const CPR_STEPS = useMemo(() => [
        { title: t('cpr_step_1_title'), text: t('cpr_step_1_text') },
        { title: t('cpr_step_2_title'), text: t('cpr_step_2_text') },
        { title: t('cpr_step_3_title'), text: t('cpr_step_3_text') },
        { title: t('cpr_step_4_title'), text: t('cpr_step_4_text') },
    ], [t]);

    const [availableVoices, setAvailableVoices] = useState<Speech.Voice[]>([]);

    useEffect(() => {
        async function fetchVoices() {
            try {
                const voices = await Speech.getAvailableVoicesAsync();
                setAvailableVoices(voices);
                console.log('Available voices:', voices.map(v => v.language));
            } catch (e) {
                console.warn('Failed to fetch voices', e);
            }
        }
        fetchVoices();
    }, []);
    const speak = (text: string) => {
        // Stop any current speech immediately
        Speech.stop();

        const currentLang = i18n.language; // 'en', 'hi', 'kn'

        // 1. Smart Voice Search (Case insensitive)
        const exactVoice = availableVoices.find(v =>
            v.language.toLowerCase().includes(currentLang.toLowerCase()) ||
            (v.name && v.name.toLowerCase().includes(currentLang.toLowerCase()))
        );

        // 2. Map generic language codes to locale-specific codes as a fallback
        const langMap: Record<string, string> = {
            'en': 'en-US',
            'hi': 'hi-IN',
            'kn': 'kn-IN'
        };
        const fallbackLang = langMap[currentLang] || 'en-US';

        const options: Speech.SpeechOptions = {
            pitch: 1.0,
            rate: 0.85, // Slightly slower for better clarity
            language: fallbackLang, // Always set a default language
        };

        if (exactVoice) {
            console.log(`Using specific voice: ${exactVoice.identifier} (${exactVoice.language})`);
            options.voice = exactVoice.identifier;
            options.language = exactVoice.language; // Explicitly sync language with voice
        } else {
            console.log(`No specific voice found for ${currentLang}, using fallback: ${fallbackLang}`);
        }

        // Small delay to ensure the engine is ready after stop()
        setTimeout(() => {
            Speech.speak(text, options);
        }, 100);
    };

    useEffect(() => {
        speak(CPR_STEPS[currentStep].text);
    }, [currentStep, CPR_STEPS]);

    const nextStep = () => {
        if (currentStep < CPR_STEPS.length - 1) {
            setCurrentStep(c => c + 1);
        } else {
            router.back();
        }
    };

    const prevStep = () => {
        if (currentStep > 0) {
            setCurrentStep(c => c - 1);
        }
    };

    const repeatStep = () => {
        speak(CPR_STEPS[currentStep].text);
    };

    return (
        <SafeAreaView style={{ flex: 1, backgroundColor: '#F9FAFB' }}>
            <StatusBar barStyle="dark-content" />

            {/* Header */}
            <View style={{ paddingHorizontal: SPACING.m, paddingTop: SPACING.xl, paddingBottom: SPACING.m, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
                <View>
                    <Text style={{ fontSize: rf(14), fontWeight: '700', color: COLORS.primary }}>{t('cpr_guidance_mode')}</Text>
                    <Text style={{ fontSize: rf(12), color: COLORS.muted }}>{t('ai_guidance')}</Text>
                </View>
                <TouchableOpacity onPress={() => router.back()}>
                    <Ionicons name="close-circle" size={rf(32)} color={COLORS.muted} />
                </TouchableOpacity>
            </View>

            <ScrollView style={{ flex: 1 }} contentContainerStyle={{ flexGrow: 1, padding: SPACING.l, alignItems: 'center' }}>
                {/* Visual Aid */}
                <View style={{ width: '100%', aspectRatio: 1.2, backgroundColor: '#FFEDD5', borderRadius: RADIUS.xl, alignItems: 'center', justifyContent: 'center', marginBottom: SPACING.xl }}>
                    <Ionicons name="body" size={rf(120)} color={COLORS.warning} />
                    {/* In a real app, this would be an illustration image */}
                </View>

                <Text style={{ fontSize: rf(24), fontWeight: '800', color: COLORS.text, textAlign: 'center', marginBottom: SPACING.m }}>
                    {CPR_STEPS[currentStep].title}
                </Text>

                <Text style={{ fontSize: rf(18), color: COLORS.muted, marginBottom: SPACING.xl, textAlign: 'center' }}>
                    {CPR_STEPS[currentStep].text}
                </Text>

                {/* Progress Dots */}
                <View style={{ flexDirection: 'row', gap: SPACING.s, marginBottom: SPACING.xl }}>
                    {CPR_STEPS.map((_, index) => (
                        <View key={index} style={{
                            width: rf(8), height: rf(8), borderRadius: rf(4),
                            backgroundColor: index === currentStep ? COLORS.primary : COLORS.border
                        }} />
                    ))}
                </View>
            </ScrollView>

            {/* Controls */}
            <View style={{ padding: SPACING.l, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', backgroundColor: 'white', borderTopColor: COLORS.border, borderTopWidth: 1 }}>
                <TouchableOpacity
                    style={{ alignItems: 'center', padding: SPACING.s }}
                    onPress={repeatStep}
                >
                    <Ionicons name="refresh-circle" size={rf(40)} color={COLORS.muted} />
                    <Text style={{ fontSize: rf(12), fontWeight: '600', color: COLORS.muted }}>{t('repeat')}</Text>
                </TouchableOpacity>

                <TouchableOpacity
                    style={{ alignItems: 'center', padding: SPACING.s }}
                    onPress={() => Speech.isSpeakingAsync().then(speaking => speaking ? Speech.stop() : speak(CPR_STEPS[currentStep].text))}
                >
                    <Ionicons name="pause-circle" size={rf(40)} color={COLORS.muted} />
                    <Text style={{ fontSize: rf(12), fontWeight: '600', color: COLORS.muted }}>Pause</Text>
                </TouchableOpacity>

                <TouchableOpacity
                    style={{
                        backgroundColor: COLORS.primary, paddingHorizontal: SPACING.xl, paddingVertical: SPACING.m,
                        borderRadius: RADIUS.full, flexDirection: 'row', alignItems: 'center'
                    }}
                    onPress={nextStep}
                >
                    <Text style={{ color: 'white', fontWeight: 'bold', marginRight: SPACING.s, fontSize: rf(16) }}>{t('next')}</Text>
                    <Ionicons name="arrow-forward" size={rf(20)} color="white" />
                </TouchableOpacity>
            </View>
        </SafeAreaView>
    );
}
