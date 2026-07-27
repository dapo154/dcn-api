
# src/screens/SOSScreen.tsx
sos_screen = """import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Animated,
  Vibration,
  Alert,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

import { useSOSStore } from '../store/sosStore';

export default function SOSScreen() {
  const navigation = useNavigation();
  const { 
    triggerSOS, 
    isPanicking, 
    emergencyContacts, 
    sosHistory,
    isSOSEnabled,
    toggleSOSEnabled,
  } = useSOSStore();
  
  const [pulseAnim] = useState(new Animated.Value(1));
  const [countdown, setCountdown] = useState(0);

  useEffect(() => {
    if (isPanicking) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, {
            toValue: 1.2,
            duration: 500,
            useNativeDriver: true,
          }),
          Animated.timing(pulseAnim, {
            toValue: 1,
            duration: 500,
            useNativeDriver: true,
          }),
        ])
      ).start();
    } else {
      pulseAnim.setValue(1);
    }
  }, [isPanicking]);

  const handleSOSPress = () => {
    if (!isSOSEnabled) {
      Alert.alert('SOS Disabled', 'Please enable SOS in settings first.');
      return;
    }

    if (emergencyContacts.length === 0) {
      Alert.alert(
        'No Emergency Contacts',
        'Please add emergency contacts before using SOS.',
        [
          { text: 'Cancel', style: 'cancel' },
          { 
            text: 'Add Contacts', 
            onPress: () => navigation.navigate('EmergencyContacts' as never) 
          },
        ]
      );
      return;
    }

    // Countdown before triggering
    setCountdown(3);
    const interval = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          triggerSOS();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const handleCancelSOS = () => {
    setCountdown(0);
    Vibration.cancel();
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Emergency SOS</Text>
        <TouchableOpacity
          style={[
            styles.toggleButton,
            isSOSEnabled ? styles.toggleActive : styles.toggleInactive,
          ]}
          onPress={() => toggleSOSEnabled(!isSOSEnabled)}
        >
          <Text style={[
            styles.toggleText,
            isSOSEnabled ? styles.toggleTextActive : styles.toggleTextInactive,
          ]}>
            {isSOSEnabled ? 'ON' : 'OFF'}
          </Text>
        </TouchableOpacity>
      </View>

      {/* SOS Button */}
      <View style={styles.sosContainer}>
        <Animated.View
          style={[
            styles.pulseRing,
            { transform: [{ scale: pulseAnim }] },
          ]}
        >
          <LinearGradient
            colors={isPanicking ? ['#ff0000', '#ff4444'] : ['#ff3d3d', '#ff6b6b']}
            style={styles.sosButton}
          >
            <TouchableOpacity
              onPress={handleSOSPress}
              disabled={isPanicking || countdown > 0}
              activeOpacity={0.8}
              style={styles.sosButtonInner}
            >
              {countdown > 0 ? (
                <Text style={styles.countdownText}>{countdown}</Text>
              ) : isPanicking ? (
                <>
                  <Ionicons name="warning" size={40} color="#fff" />
                  <Text style={styles.sosButtonText}>SOS ACTIVE</Text>
                </>
              ) : (
                <>
                  <Ionicons name="alert-circle" size={40} color="#fff" />
                  <Text style={styles.sosButtonText}>PRESS FOR SOS</Text>
                </>
              )}
            </TouchableOpacity>
          </LinearGradient>
        </Animated.View>

        {countdown > 0 && (
          <TouchableOpacity style={styles.cancelButton} onPress={handleCancelSOS}>
            <Text style={styles.cancelText}>Cancel</Text>
          </TouchableOpacity>
        )}

        {isPanicking && (
          <View style={styles.sosStatus}>
            <Ionicons name="radio-button-on" size={16} color="#ff3d3d" />
            <Text style={styles.sosStatusText}>
              Broadcasting distress signal...
            </Text>
          </View>
        )}
      </View>

      {/* Emergency Contacts */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Emergency Contacts</Text>
          <TouchableOpacity
            onPress={() => navigation.navigate('EmergencyContacts' as never)}
          >
            <Text style={styles.sectionAction}>Manage</Text>
          </TouchableOpacity>
        </View>

        {emergencyContacts.length === 0 ? (
          <View style={styles.emptyContacts}>
            <Ionicons name="people-outline" size={32} color="#4a5a70" />
            <Text style={styles.emptyText}>No emergency contacts added</Text>
            <TouchableOpacity
              style={styles.addButton}
              onPress={() => navigation.navigate('EmergencyContacts' as never)}
            >
              <Text style={styles.addButtonText}>Add Contacts</Text>
            </TouchableOpacity>
          </View>
        ) : (
          emergencyContacts.map((contact) => (
            <View key={contact.id} style={styles.contactCard}>
              <View style={styles.contactAvatar}>
                <Text style={styles.contactInitial}>
                  {contact.name.charAt(0).toUpperCase()}
                </Text>
              </View>
              <View style={styles.contactInfo}>
                <Text style={styles.contactName}>{contact.name}</Text>
                <Text style={styles.contactPhone}>{contact.phone}</Text>
                <Text style={styles.contactRelation}>{contact.relationship}</Text>
              </View>
              <TouchableOpacity style={styles.callButton}>
                <Ionicons name="call" size={20} color="#00e676" />
              </TouchableOpacity>
            </View>
          ))
        )}
      </View>

      {/* SOS History */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>SOS History</Text>
        {sosHistory.length === 0 ? (
          <Text style={styles.emptyText}>No SOS events recorded</Text>
        ) : (
          sosHistory.slice(0, 5).map((event) => (
            <View key={event.id} style={styles.historyItem}>
              <View style={styles.historyIcon}>
                <Ionicons name="warning" size={16} color="#ff3d3d" />
              </View>
              <View style={styles.historyInfo}>
                <Text style={styles.historyTitle}>SOS Triggered</Text>
                <Text style={styles.historyTime}>
                  {new Date(event.timestamp).toLocaleString()}
                </Text>
              </View>
              <View style={[
                styles.historyStatus,
                event.status === 'resolved' && styles.historyStatusResolved,
              ]}>
                <Text style={[
                  styles.historyStatusText,
                  event.status === 'resolved' && styles.historyStatusTextResolved,
                ]}>
                  {event.status}
                </Text>
              </View>
            </View>
          ))
        )}
      </View>
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
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    marginBottom: 24,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: '800',
    color: '#f0f4f8',
  },
  toggleButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 1,
  },
  toggleActive: {
    backgroundColor: 'rgba(0,230,118,0.15)',
    borderColor: 'rgba(0,230,118,0.3)',
  },
  toggleInactive: {
    backgroundColor: 'rgba(255,61,61,0.15)',
    borderColor: 'rgba(255,61,61,0.3)',
  },
  toggleText: {
    fontWeight: '700',
    fontSize: 12,
  },
  toggleTextActive: {
    color: '#00e676',
  },
  toggleTextInactive: {
    color: '#ff3d3d',
  },
  sosContainer: {
    alignItems: 'center',
    marginBottom: 32,
  },
  pulseRing: {
    shadowColor: '#ff3d3d',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.5,
    shadowRadius: 20,
    elevation: 10,
  },
  sosButton: {
    width: 180,
    height: 180,
    borderRadius: 90,
    alignItems: 'center',
    justifyContent: 'center',
  },
  sosButtonInner: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  sosButtonText: {
    color: '#fff',
    fontWeight: '800',
    fontSize: 14,
    marginTop: 8,
  },
  countdownText: {
    color: '#fff',
    fontWeight: '800',
    fontSize: 48,
  },
  cancelButton: {
    marginTop: 16,
    paddingHorizontal: 24,
    paddingVertical: 10,
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderRadius: 20,
  },
  cancelText: {
    color: '#f0f4f8',
    fontWeight: '600',
  },
  sosStatus: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginTop: 16,
    backgroundColor: 'rgba(255,61,61,0.1)',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  sosStatusText: {
    color: '#ff3d3d',
    fontWeight: '600',
    fontSize: 13,
  },
  section: {
    paddingHorizontal: 20,
    marginBottom: 24,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#f0f4f8',
  },
  sectionAction: {
    color: '#d4a853',
    fontWeight: '600',
    fontSize: 14,
  },
  emptyContacts: {
    backgroundColor: 'rgba(10,20,40,0.65)',
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.06)',
  },
  emptyText: {
    color: '#4a5a70',
    textAlign: 'center',
    marginTop: 8,
    marginBottom: 16,
  },
  addButton: {
    backgroundColor: '#d4a853',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 10,
  },
  addButtonText: {
    color: '#050a14',
    fontWeight: '700',
  },
  contactCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(10,20,40,0.65)',
    borderRadius: 16,
    padding: 16,
    marginBottom: 8,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.06)',
  },
  contactAvatar: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: 'rgba(212,168,83,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  contactInitial: {
    color: '#d4a853',
    fontWeight: '800',
    fontSize: 18,
  },
  contactInfo: {
    flex: 1,
    marginLeft: 12,
  },
  contactName: {
    color: '#f0f4f8',
    fontWeight: '700',
    fontSize: 15,
  },
  contactPhone: {
    color: '#8a9ab0',
    fontSize: 13,
    marginTop: 2,
  },
  contactRelation: {
    color: '#4a5a70',
    fontSize: 12,
    marginTop: 2,
  },
  callButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(0,230,118,0.15)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  historyItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(10,20,40,0.65)',
    borderRadius: 12,
    padding: 12,
    marginBottom: 8,
  },
  historyIcon: {
    width: 32,
    height: 32,
    borderRadius: 8,
    backgroundColor: 'rgba(255,61,61,0.1)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  historyInfo: {
    flex: 1,
    marginLeft: 12,
  },
  historyTitle: {
    color: '#f0f4f8',
    fontWeight: '600',
    fontSize: 14,
  },
  historyTime: {
    color: '#8a9ab0',
    fontSize: 12,
    marginTop: 2,
  },
  historyStatus: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
    backgroundColor: 'rgba(255,61,61,0.15)',
  },
  historyStatusResolved: {
    backgroundColor: 'rgba(0,230,118,0.15)',
  },
  historyStatusText: {
    color: '#ff3d3d',
    fontSize: 10,
    fontWeight: '700',
  },
  historyStatusTextResolved: {
    color: '#00e676',
  },
});
"""

with open(f'{app_dir}/src/screens/SOSScreen.tsx', 'w') as f:
    f.write(sos_screen)

print("SOSScreen created")
