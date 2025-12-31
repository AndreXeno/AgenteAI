import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import MentalWellbeing from './pages/MentalWellbeing';
import DiaryPage from './pages/DiaryPage';
import PsychologistProfile from './pages/PsychologistProfile';
import ContactPsychologist from './pages/ContactPsychologist';
import Account from './pages/Account';
import AIChat from './pages/AIChat';
import Nutrition from './pages/Nutrition';
import BoxSetup from './pages/BoxSetup';
import PaymentDetails from './pages/PaymentDetails';
import TrackBox from './pages/TrackBox';
import ShareRecipe from './pages/ShareRecipe';
import TrainingOnboardingPage from './pages/TrainingOnboardingPage';
import TrainingDashboardPage from './pages/TrainingDashboardPage';
import WorkoutSessionPage from './pages/WorkoutSessionPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/mental-wellbeing" element={<MentalWellbeing />} />
        <Route path="/training" element={<TrainingDashboardPage />} />
        <Route path="/training/setup" element={<TrainingOnboardingPage />} />
        <Route path="/training/session" element={<WorkoutSessionPage />} />
        <Route path="/diary" element={<DiaryPage />} />
        <Route path="/psychologist/:id" element={<PsychologistProfile />} />
        <Route path="/psychologist/:id/contact" element={<ContactPsychologist />} />
        <Route path="/account" element={<Account />} />
        <Route path="/chat" element={<AIChat />} />
        <Route path="/nutrition" element={<Nutrition />} />
        <Route path="/box/setup" element={<BoxSetup />} />
        <Route path="/box/pagamento" element={<PaymentDetails />} />
        <Route path="/box/tracking" element={<TrackBox />} />
        <Route path="/share-recipe" element={<ShareRecipe />} />
      </Routes>
    </Router>
  );
}

export default App;
