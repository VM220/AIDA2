import numpy as np

# Define probabilities as given in the image
P_A = {True: 0.8, False: 0.2}
P_C = {True: 0.5, False: 0.5}
P_G_given_A_C = {
    ('Good', True, True): 0.9,
    ('Good', True, False): 0.7,
    ('Good', False, True): 0.6,
    ('Good', False, False): 0.3,
    ('OK', True, True): 0.1,
    ('OK', True, False): 0.3,
    ('OK', False, True): 0.4,
    ('OK', False, False): 0.7
}
P_S_given_G = {
    'Good': {True: 0.7, False: 0.3},
    'OK': {True: 0.3, False: 0.7}
}
P_J_given_G = {
    'Good': {True: 0.8, False: 0.2},
    'OK': {True: 0.2, False: 0.8}
}

# Monte Carlo simulation to estimate P(Good | A=True, C=True) and P(S | G), P(J | G)
def monte_carlo_simulation(num_samples=10000):
    count_good_given_evidence = 0
    count_ok_given_evidence = 0
    count_startup_given_good = 0
    count_startup_given_ok = 0
    count_job_given_good = 0
    count_job_given_ok = 0
    count_evidence = 0
    
    for _ in range(num_samples):
        # Sample Aptitude Skills
        aptitude = np.random.rand() < P_A[True]
        # Sample Coding Skills
        coding = np.random.rand() < P_C[True]
        
        # Check evidence
        if aptitude and coding:  # A=True, C=True
            count_evidence += 1
            
            # Sample Grade based on A and C
            is_good = np.random.rand() < P_G_given_A_C[('Good', aptitude, coding)]
            grade = 'Good' if is_good else 'OK'
            
            # Count occurrences of each grade
            if grade == 'Good':
                count_good_given_evidence += 1
            else:
                count_ok_given_evidence += 1
            
            # Sample Start a Startup given Grade
            startup = np.random.rand() < P_S_given_G[grade][True]
            # Sample Go for Job given Grade
            job = np.random.rand() < P_J_given_G[grade][True]
            
            # Accumulate counts based on the grade
            if grade == 'Good':
                if startup:
                    count_startup_given_good += 1
                if job:
                    count_job_given_good += 1
            else:
                if startup:
                    count_startup_given_ok += 1
                if job:
                    count_job_given_ok += 1

    # Calculate conditional probabilities
    if count_good_given_evidence > 0:
        p_startup_given_good = count_startup_given_good / count_good_given_evidence
        p_job_given_good = count_job_given_good / count_good_given_evidence
    else:
        p_startup_given_good = 0
        p_job_given_good = 0

    if count_ok_given_evidence > 0:
        p_startup_given_ok = count_startup_given_ok / count_ok_given_evidence
        p_job_given_ok = count_job_given_ok / count_ok_given_evidence
    else:
        p_startup_given_ok = 0
        p_job_given_ok = 0
    
    # Return results
    return {
        "P(Good | A=True, C=True)": count_good_given_evidence / count_evidence if count_evidence > 0 else 0,
        "P(Startup | Good)": p_startup_given_good,
        "P(Job | Good)": p_job_given_good,
        "P(Startup | OK)": p_startup_given_ok,
        "P(Job | OK)": p_job_given_ok
    }

# Run simulation
results = monte_carlo_simulation()
print("Results:")
print(f"Estimated P(Good | A=True, C=True): {results['P(Good | A=True, C=True)']}")
print(f"Estimated P(Startup | Good): {results['P(Startup | Good)']}")
print(f"Estimated P(Job | Good): {results['P(Job | Good)']}")
print(f"Estimated P(Startup | OK): {results['P(Startup | OK)']}")
print(f"Estimated P(Job | OK): {results['P(Job | OK)']}")
