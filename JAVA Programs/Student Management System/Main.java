// Title: Student Management System
// Description: A simple student management system that allows you to add, update, delete, view student details, and view a list of all students.

import java.util.*;

class Student {
  private String enrollId;
  private String name;
  private String dob;
  private String email;
  private long phone;
  private String branch;
  private String course;
  private int semester;

  // Constructor
  public Student(String enrollId, String name, String dob, String email, long phone, String branch, String course,
      int semester) {
    this.enrollId = enrollId;
    this.name = name;
    this.dob = dob;
    this.email = email;
    this.phone = phone;
    this.branch = branch;
    this.course = course;
    this.semester = semester;
  }

  // Getters
  public String getEnrollId() {
    return enrollId;
  }
  public String getName() {
    return name;
  }
  public String getDob() {
    return dob;
  }
  public String getEmail() {
    return email;
  }
  public long getPhone() {
    return phone;
  }
  public String getBranch() {
    return branch;
  }
  public String getCourse() {
    return course;
  }
  public int getSemester() {
    return semester;
  }

  // Setters
  public void setEnrollId(String enrollId) {
    this.enrollId = enrollId;
  }
  public void setName(String name) {
    this.name = name;
  }
  public void setDob(String dob) {
    this.dob = dob;
  }
  public void setEmail(String email) {
    this.email = email;
  }
  public void setPhone(long phone) {
    this.phone = phone;
  }
  public void setBranch(String branch) {
    this.branch = branch;
  }
  public void setCourse(String course) {
    this.course = course;
  }
  public void setSemester(int semester) {
    this.semester = semester;
  }

  // toString
  @Override
  public String toString() {
    return "Student{" +
        "enrollId=" + enrollId +
        ", name='" + name + '\'' +
        ", dob='" + dob + '\'' +
        ", email='" + email + '\'' +
        ", phone=" + phone +
        ", branch='" + branch + '\'' +
        ", course='" + course + '\'' +
        ", semester=" + semester +
        '}';
  }
}

public class Main {
  public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);
    List<Student> students = new ArrayList<>();

    while (true) {
      System.out.println("===== Student Management System =====");
      System.out.println("1. Student Menu");
      System.out.println("2. Exit");
      System.out.print("Enter your choice: ");
      int choice = scanner.nextInt();

      switch (choice) {
        case 1:
          studentMenu(scanner, students);
          break;
        case 2:
          System.out.println("Goodbye! Have a nice day.");
          System.out.println("Exiting...");
          System.exit(0);
          break;
        default:
          System.out.println("Invalid choice. Please try again.\n");
      }
    }
  }

  private static void studentMenu(Scanner scanner, List<Student> students) {
    while (true) {
      System.out.println("===== Student Menu =====");
      System.out.println("1. Add Student");
      System.out.println("2. Update Student");
      System.out.println("3. Delete Student");
      System.out.println("4. View Student Details");
      System.out.println("5. View All Students");
      System.out.println("6. Back");
      System.out.print("Enter your choice: ");
      int choice = scanner.nextInt();

      switch (choice) {
        case 1:
          addStudent(scanner, students);
          break;
        case 2:
          updateStudent(scanner, students);
          break;
        case 3:
          deleteStudent(scanner, students);
          break;
        case 4:
          viewStudentDetails(scanner, students);
          break;
        case 5:
          viewAllStudents(scanner, students);
          break;
        case 6:
          return;
        default:
          System.out.println("Invalid choice. Please try again.\n");
      }
    }
  }

  private static void addStudent(Scanner scanner, List<Student> students) {
    System.out.print("Enter Enrollment No.: ");
    String enrollId = scanner.next();
    System.out.print("Enter Name: ");
    String name = scanner.next();
    System.out.print("Enter Date of Birth: ");
    String dob = scanner.next();
    System.out.print("Enter Email: ");
    String email = scanner.next();
    System.out.print("Enter Phone No.: ");
    long phone = scanner.nextLong();
    System.out.print("Enter Branch: ");
    String branch = scanner.next();
    System.out.print("Enter Course: ");
    String course = scanner.next();
    System.out.print("Enter Semester: ");
    int semester = scanner.nextInt();
    Student student = new Student(enrollId, name, dob, email, phone, branch, course, semester);
    students.add(student);
    System.out.println("Student added successfully.\n");
  }

  private static void updateStudent(Scanner scanner, List<Student> students) {
    System.out.print("Enter Enrollment No. of student to update: ");
    String enrollId = scanner.next();

    for (Student student : students) {
      if (enrollId.equals(student.getEnrollId())) {
        System.out.println("===== Current Details =====");
        System.out.println("Enrollment No.: " + student.getEnrollId());
        System.out.println("Name: " + student.getName());
        System.out.println("Date of Birth: " + student.getDob());
        System.out.println("Email: " + student.getEmail());
        System.out.println("Phone No.: " + student.getPhone());
        System.out.println("Branch: " + student.getBranch());
        System.out.println("Course: " + student.getCourse());
        System.out.println("Semester: " + student.getSemester());

        System.out.println("\n===== Enter New Details =====");
        System.out.print("Enter Name: ");
        student.setName(scanner.next());
        System.out.print("Enter Date of Birth: ");
        student.setDob(scanner.next());
        System.out.print("Enter Email: ");
        student.setEmail(scanner.next());
        System.out.print("Enter Phone No.: ");
        student.setPhone(scanner.nextLong());
        System.out.print("Enter Branch: ");
        student.setBranch(scanner.next());
        System.out.print("Enter Course: ");
        student.setCourse(scanner.next());
        System.out.print("Enter Semester: ");
        student.setSemester(scanner.nextInt());
        System.out.println("Student details updated successfully.\n");
        return;
      }
    }
    System.out.println("Student with Enrollment No. " + enrollId + " not found.\n");
  }

  private static void deleteStudent(Scanner scanner, List<Student> students) {
    System.out.print("Enter Enrollment No. of student to delete: ");
    String enrollId = scanner.next();
    for (Student student : students) {
      if (enrollId.equals(student.getEnrollId())) {
        students.remove(student);
        System.out.println("Student deleted successfully.\n");
        return;
      }
    }
    System.out.println("Student with Enrollment No. " + enrollId + " not found.\n");
  }

  private static void viewAllStudents(Scanner scanner, List<Student> students) {
    if (students.isEmpty()) {
      System.out.println("No students found.\n");
    } else {
      System.out.println("===== List of Students =====\n");
      System.out.println("Enrollment No." + "\t\t" + "Name" + "\t\t" + "Branch");
      System.out.println("--------------------------------------------------");
      for (Student student : students) {
        System.out.println(student.getEnrollId() + "\t\t\t" + student.getName() + "\t\t" + student.getBranch());
      }
      System.out.println("--------------------------------------------------");
      scanner.nextLine();
      System.out.println("Press Enter to continue...");
      scanner.nextLine();
    }
  }

  private static void viewStudentDetails(Scanner scanner, List<Student> students) {
    System.out.print("Enter Enrollment No. of student: ");
    String enrollId = scanner.next();
    scanner.nextLine();

    for (Student student : students) {
      if (enrollId.equals(student.getEnrollId())) {
        System.out.println("===== Details of " + student.getName() + " =====");
        System.out.println("Enrollment No.: " + student.getEnrollId());
        System.out.println("Name: " + student.getName());
        System.out.println("Date of Birth: " + student.getDob());
        System.out.println("Email: " + student.getEmail());
        System.out.println("Phone No.: " + student.getPhone());
        System.out.println("Branch: " + student.getBranch());
        System.out.println("Course: " + student.getCourse());
        System.out.println("Semester: " + student.getSemester());
        System.out.println("Press Enter to continue...");
        scanner.nextLine();
        
        return;
      }
    }
    System.out.println("Student with Enrollment No. " + enrollId + " not found.");
  }
}