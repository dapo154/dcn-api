
# src/screens/RegisterScreen.tsx
register_screen = """import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
  ScrollView,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation, useRoute } from '@react-navigation/native';

import { useAuthStore } from '../store/authStore';

export default function RegisterScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { register } = useAuthStore();
  
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [referralCode, setReferralCode] = useState((route.params as any)?.ref || '');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleRegister = async () => {
    if (!name || !email || !password) {
      setError('Please fill in all required fields');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      await register(name, email, password, referralCode || undefined);
    } catch (err: any) {
      setError(err.message || 'Registration failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
          >
            <Ionicons name="arrow-back" size={24} color="#f0f4f8" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Create Account</Text>
          <Text style={styles.headerSubtitle}>
            Join DCN and get 50 free credits
          </Text>
        </View>

        {/* Form */}
        <View style={styles.form}>
          {error ? (
            <View style={styles.errorContainer}>
              <Ionicons name="alert-circle" size={16} color="#ff3d3d" />
              <Text style={styles.errorText}>{error}</Text>
            </View>
          ) : null}

          <View style={styles.inputContainer}>
            <Ionicons name="person-outline" size={20} color="#4a5a70" />
            <TextInput
              style={styles.input}
              placeholder="Full name"
              placeholderTextColor="#4a5a70"
              value={name}
              onChangeText={setName}
              autoCapitalize="words"
            />
          </View>

          <View style={styles.inputContainer}>
            <Ionicons name="mail-outline" size={20} color="#4a5a70" />
            <TextInput
              style={styles.input}
              placeholder="Email address"
              placeholderTextColor="#4a5a70"
              value={email}
              onChangeText={setEmail}
              autoCapitalize="none"
              keyboardType="email-address"
            />
          </View>

          <View style={styles.inputContainer}>
            <Ionicons name="lock-closed-outline" size={20} color="#4a5a70" />
            <TextInput
              style={styles.input}
              placeholder="Password"
              placeholderTextColor="#4a5a70"
              value={password}
              onChangeText={setPassword}
              secureTextEntry={!showPassword}
            />
            <TouchableOpacity onPress={() => setShowPassword(!showPassword)}>
              <Ionicons
                name={showPassword ? 'eye-off-outline' : 'eye-outline'}
                size={20}
                color="#4a5a70"
              />
            </TouchableOpacity>
          </View>

          <View style={styles.inputContainer}>
            <Ionicons name="lock-closed-outline" size={20} color="#4a5a70" />
            <TextInput
              style={styles.input}
              placeholder="Confirm password"
              placeholderTextColor="#4a5a70"
              value={confirmPassword}
              onChangeText={setConfirmPassword}
              secureTextEntry={!showPassword}
            />
          </View>

          <View style={styles.inputContainer}>
            <Ionicons name="gift-outline" size={20} color="#4a5a70" />
            <TextInput
              style={styles.input}
              placeholder="Referral code (optional)"
              placeholderTextColor="#4a5a70"
              value={referralCode}
              onChangeText={setReferralCode}
              autoCapitalize="characters"
            />
          </View>

          <TouchableOpacity
            style={styles.registerButton}
            onPress={handleRegister}
            disabled={isLoading}
            activeOpacity={0.8}
          >
            <LinearGradient
              colors={['#d4a853', '#f0c96a']}
              style={styles.registerGradient}
            >
              {isLoading ? (
                <ActivityIndicator color="#050a14" />
              ) : (
                <Text style={styles.registerButtonText}>Create Account</Text>
              )}
            </LinearGradient>
          </TouchableOpacity>
        </View>

        {/* Footer */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>Already have an account?</Text>
          <TouchableOpacity onPress={() => navigation.navigate('Login' as never)}>
            <Text style={styles.footerLink}>Sign In</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#050a14',
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    paddingHorizontal: 32,
    paddingVertical: 40,
  },
  header: {
    marginBottom: 32,
  },
  backButton: {
    marginBottom: 16,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: '800',
    color: '#f0f4f8',
  },
  headerSubtitle: {
    color: '#8a9ab0',
    fontSize: 15,
    marginTop: 8,
  },
  form: {
    gap: 16,
  },
  errorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: 'rgba(255,61,61,0.1)',
    padding: 12,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: 'rgba(255,61,61,0.2)',
  },
  errorText: {
    color: '#ff3d3d',
    fontSize: 13,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(10,20,40,0.8)',
    borderRadius: 14,
    paddingHorizontal: 16,
    height: 56,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.06)',
    gap: 12,
  },
  input: {
    flex: 1,
    color: '#f0f4f8',
    fontSize: 15,
  },
  registerButton: {
    borderRadius: 14,
    overflow: 'hidden',
    marginTop: 8,
  },
  registerGradient: {
    height: 56,
    alignItems: 'center',
    justifyContent: 'center',
  },
  registerButtonText: {
    color: '#050a14',
    fontSize: 16,
    fontWeight: '800',
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 6,
    marginTop: 32,
  },
  footerText: {
    color: '#8a9ab0',
    fontSize: 14,
  },
  footerLink: {
    color: '#d4a853',
    fontSize: 14,
    fontWeight: '700',
  },
});
"""

with open(f'{app_dir}/src/screens/RegisterScreen.tsx', 'w') as f:
    f.write(register_screen)

# src/screens/EmergencyContactsScreen.tsx
emergency_contacts = """import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  FlatList,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

import { useSOSStore } from '../store/sosStore';

export default function EmergencyContactsScreen() {
  const navigation = useNavigation();
  const { emergencyContacts, addEmergencyContact, removeEmergencyContact } = useSOSStore();
  
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [relationship, setRelationship] = useState('');
  const [isAdding, setIsAdding] = useState(false);

  const handleAdd = async () => {
    if (!name || !phone) {
      Alert.alert('Error', 'Name and phone are required');
      return;
    }

    await addEmergencyContact({
      id: Date.now().toString(),
      name,
      phone,
      relationship: relationship || 'Other',
    });

    setName('');
    setPhone('');
    setRelationship('');
    setIsAdding(false);
  };

  const handleRemove = (id: string, name: string) => {
    Alert.alert(
      'Remove Contact',
      `Remove ${name} from emergency contacts?`,
      [
        { text: 'Cancel', style: 'cancel' },
        { 
          text: 'Remove', 
          style: 'destructive',
          onPress: () => removeEmergencyContact(id),
        },
      ]
    );
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Ionicons name="arrow-back" size={24} color="#f0f4f8" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Emergency Contacts</Text>
        <TouchableOpacity onPress={() => setIsAdding(!isAdding)}>
          <Ionicons name={isAdding ? 'close' : 'add'} size={24} color="#d4a853" />
        </TouchableOpacity>
      </View>

      {/* Add Form */}
      {isAdding && (
        <View style={styles.addForm}>
          <TextInput
            style={styles.input}
            placeholder="Contact name"
            placeholderTextColor="#4a5a70"
            value={name}
            onChangeText={setName}
          />
          <TextInput
            style={styles.input}
            placeholder="Phone number"
            placeholderTextColor="#4a5a70"
            value={phone}
            onChangeText={setPhone}
            keyboardType="phone-pad"
          />
          <TextInput
            style={styles.input}
            placeholder="Relationship (e.g., Family, Friend)"
            placeholderTextColor="#4a5a70"
            value={relationship}
            onChangeText={setRelationship}
          />
          <TouchableOpacity style={styles.addButton} onPress={handleAdd}>
            <Text style={styles.addButtonText}>Add Contact</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Contacts List */}
      <FlatList
        data={emergencyContacts}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.list}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Ionicons name="people-outline" size={48} color="#4a5a70" />
            <Text style={styles.emptyText}>No emergency contacts</Text>
            <Text style={styles.emptySubtext}>
              Add contacts who will be notified when you trigger SOS
            </Text>
          </View>
        }
        renderItem={({ item }) => (
          <View style={styles.contactCard}>
            <View style={styles.contactAvatar}>
              <Text style={styles.contactInitial}>
                {item.name.charAt(0).toUpperCase()}
              </Text>
            </View>
            <View style={styles.contactInfo}>
              <Text style={styles.contactName}>{item.name}</Text>
              <Text style={styles.contactPhone}>{item.phone}</Text>
              <Text style={styles.contactRelation}>{item.relationship}</Text>
            </View>
            <TouchableOpacity
              style={styles.removeButton}
              onPress={() => handleRemove(item.id, item.name)}
            >
              <Ionicons name="trash-outline" size={20} color="#ff3d3d" />
            </TouchableOpacity>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#050a14',
    paddingTop: 60,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#f0f4f8',
  },
  addForm: {
    paddingHorizontal: 20,
    gap: 12,
    marginBottom: 20,
  },
  input: {
    backgroundColor: 'rgba(10,20,40,0.8)',
    borderRadius: 12,
    paddingHorizontal: 16,
    height: 50,
    color: '#f0f4f8',
    fontSize: 15,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.06)',
  },
  addButton: {
    backgroundColor: '#d4a853',
    borderRadius: 12,
    height: 50,
    alignItems: 'center',
    justifyContent: 'center',
  },
  addButtonText: {
    color: '#050a14',
    fontWeight: '700',
    fontSize: 15,
  },
  list: {
    paddingHorizontal: 20,
    paddingBottom: 32,
  },
  emptyContainer: {
    alignItems: 'center',
    paddingVertical: 60,
  },
  emptyText: {
    color: '#8a9ab0',
    fontSize: 16,
    fontWeight: '600',
    marginTop: 16,
  },
  emptySubtext: {
    color: '#4a5a70',
    fontSize: 13,
    textAlign: 'center',
    marginTop: 8,
    paddingHorizontal: 40,
  },
  contactCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(10,20,40,0.65)',
    borderRadius: 16,
    padding: 16,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.06)',
  },
  contactAvatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: 'rgba(212,168,83,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  contactInitial: {
    color: '#d4a853',
    fontWeight: '800',
    fontSize: 20,
  },
  contactInfo: {
    flex: 1,
    marginLeft: 14,
  },
  contactName: {
    color: '#f0f4f8',
    fontWeight: '700',
    fontSize: 16,
  },
  contactPhone: {
    color: '#8a9ab0',
    fontSize: 14,
    marginTop: 2,
  },
  contactRelation: {
    color: '#4a5a70',
    fontSize: 12,
    marginTop: 2,
  },
  removeButton: {
    width: 40,
    height: 40,
    borderRadius: 10,
    backgroundColor: 'rgba(255,61,61,0.1)',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
"""

with open(f'{app_dir}/src/screens/EmergencyContactsScreen.tsx', 'w') as f:
    f.write(emergency_contacts)

# src/screens/DataPlansScreen.tsx
data_plans = """import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

const PLANS = [
  {
    id: 'basic',
    name: 'Basic',
    data: '5GB',
    price: 500,
    duration: '30 days',
    features: ['Standard speed', '1 device', 'Email support'],
    color: ['#00e5ff', '#00b8d4'],
  },
  {
    id: 'standard',
    name: 'Standard',
    data: '20GB',
    price: 1500,
    duration: '30 days',
    features: ['High speed', '3 devices', 'SOS priority', 'Community alerts'],
    color: ['#d4a853', '#f0c96a'],
    popular: true,
  },
  {
    id: 'premium',
    name: 'Premium',
    data: '100GB',
    price: 5000,
    duration: '30 days',
    features: ['Ultra speed', '5 devices', 'SOS priority', 'Mesh network', '4K streaming'],
    color: ['#00e676', '#00c853'],
  },
  {
    id: 'unlimited',
    name: 'Unlimited',
    data: '∞',
    price: 15000,
    duration: '30 days',
    features: ['Unlimited data', '10 devices', 'All features', 'Dedicated support', 'Business tools'],
    color: ['#ff3d3d', '#ff6b6b'],
  },
];

export default function DataPlansScreen() {
  const navigation = useNavigation();

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Ionicons name="arrow-back" size={24} color="#f0f4f8" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Data Plans</Text>
        <View style={{ width: 24 }} />
      </View>

      {/* Subtitle */}
      <Text style={styles.subtitle}>
        Choose a plan that fits your needs. All plans include SOS emergency features.
      </Text>

      {/* Plans */}
      {PLANS.map((plan) => (
        <TouchableOpacity
          key={plan.id}
          style={[styles.planCard, plan.popular && styles.planCardPopular]}
          activeOpacity={0.9}
        >
          <LinearGradient
            colors={plan.color.map(c => c + '15') as [string, string]}
            style={styles.planGradient}
          >
            {plan.popular && (
              <View style={[styles.popularBadge, { backgroundColor: plan.color[0] + '30' }]}>
                <Text style={[styles.popularText, { color: plan.color[0] }]}>MOST POPULAR</Text>
              </View>
            )}

            <View style={styles.planHeader}>
              <View>
                <Text style={styles.planName}>{plan.name}</Text>
                <Text style={styles.planData}>{plan.data}</Text>
              </View>
              <View style={styles.priceContainer}>
                <Text style={styles.priceCurrency}>₦</Text>
                <Text style={styles.priceAmount}>{plan.price.toLocaleString()}</Text>
                <Text style={styles.pricePeriod}>/{plan.duration}</Text>
              </View>
            </View>

            <View style={styles.featuresList}>
              {plan.features.map((feature, idx) => (
                <View key={idx} style={styles.featureItem}>
                  <Ionicons name="checkmark-circle" size={16} color={plan.color[0]} />
                  <Text style={styles.featureText}>{feature}</Text>
                </View>
              ))}
            </View>

            <TouchableOpacity
              style={[styles.buyButton, { backgroundColor: plan.color[0] }]}
            >
              <Text style={styles.buyButtonText}>Subscribe</Text>
            </TouchableOpacity>
          </LinearGradient>
        </TouchableOpacity>
      ))}

      {/* Footer Note */}
      <View style={styles.footerNote}>
        <Ionicons name="information-circle" size={16} color="#4a5a70" />
        <Text style={styles.footerNoteText}>
          Plans auto-renew monthly. Cancel anytime. Data rolls over for 7 days.
        </Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#050a14',
    paddingTop: 60,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    marginBottom: 8,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '800',
    color: '#f0f4f8',
  },
  subtitle: {
    color: '#8a9ab0',
    fontSize: 14,
    paddingHorizontal: 20,
    marginBottom: 24,
    lineHeight: 20,
  },
  planCard: {
    marginHorizontal: 20,
    marginBottom: 16,
    borderRadius: 20,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.06)',
  },
  planCardPopular: {
    borderColor: 'rgba(212,168,83,0.3)',
  },
  planGradient: {
    padding: 24,
  },
  popularBadge: {
    alignSelf: 'flex-start',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
    marginBottom: 16,
  },
  popularText: {
    fontSize: 10,
    fontWeight: '800',
    letterSpacing: 1,
  },
  planHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 20,
  },
  planName: {
    color: '#f0f4f8',
    fontSize: 20,
    fontWeight: '800',
  },
  planData: {
    color: '#8a9ab0',
    fontSize: 14,
    marginTop: 4,
  },
  priceContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  priceCurrency: {
    color: '#f0f4f8',
    fontSize: 16,
    fontWeight: '600',
    marginTop: 4,
  },
  priceAmount: {
    color: '#f0f4f8',
    fontSize: 28,
    fontWeight: '800',
  },
  pricePeriod: {
    color: '#4a5a70',
    fontSize: 13,
    marginTop: 8,
  },
  featuresList: {
    gap: 10,
    marginBottom: 20,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  featureText: {
    color: '#8a9ab0',
    fontSize: 14,
  },
  buyButton: {
    borderRadius: 12,
    height: 50,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buyButtonText: {
    color: '#050a14',
    fontWeight: '800',
    fontSize: 15,
  },
  footerNote: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingHorizontal: 20,
    paddingVertical: 24,
  },
  footerNoteText: {
    color: '#4a5a70',
    fontSize: 12,
    flex: 1,
    lineHeight: 18,
  },
});
"""

with open(f'{app_dir}/src/screens/DataPlansScreen.tsx', 'w') as f:
    f.write(data_plans)

print("All remaining screens created")
