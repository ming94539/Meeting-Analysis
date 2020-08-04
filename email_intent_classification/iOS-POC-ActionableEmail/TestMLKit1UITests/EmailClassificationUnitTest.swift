//
//  EmailClassificationUnitTest.swift
//  TestMLKit1UITests
//
//  Created by kurtn on 7/13/17.
//  Copyright © 2017 kurtn. All rights reserved.
//

import XCTest
import TestMLKit1
//@testable import TestMLKit1

class EmailClassificationUnitTest: XCTestCase {
    
    let classificationEngine = EmailClassificationEngine()
    
    override func setUp() {
        super.setUp()
        // Put setup code here. This method is called before the invocation of each test method in the class.
    }
    
    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        super.tearDown()
    }
    
    func testEmailRequiresResponse() {
        classificationEngine.emailRequiresResponse(text: "The brown fox jumped.  The car is blue!")
    }
    
}
