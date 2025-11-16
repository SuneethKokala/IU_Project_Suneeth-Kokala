
##  Installation

'''bash
# Clone and setup
cd automated-safety-monitoring
pip install -r requirements.txt

# Add employee photos (format: EMP001_John_Doe.jpg)
# Train face recognition
python run.py train-faces
'''

## Usage

### Dashboard
'''bash
python run.py dashboard
'''
-**Access:** http://localhost:3001
**Login:** supervisor / admin123

### Camera Detection
'''bash
python run.py camera
'''
- **API:** http://localhost:8000/docs

