// Function to create a resource item
function createResourceItem(group, link, title, description) {
    // Create the main div element with the class 'resource-item' and the data-group attribute
    const resourceItem = document.createElement('div');
    resourceItem.className = 'resource-item';
    resourceItem.setAttribute('data-group', group);
    resourceItem.textContent = group;

    // Create the anchor element
    const anchor = document.createElement('a');
    anchor.href = link;
    anchor.target = '_blank';
    anchor.rel = 'noopener noreferrer';

    // Create the resource card div element with the class 'resource-card'
    const resourceCard = document.createElement('div');
    resourceCard.className = 'resource-card p-6 bg-gray-100 rounded-lg shadow-lg';

    // Create and append the title element
    const titleElement = document.createElement('h2');
    titleElement.className = 'mb-4 text-xl font-bold';
    titleElement.textContent = title;
    resourceCard.appendChild(titleElement);

    // Create and append the description element
    const descriptionElement = document.createElement('p');
    descriptionElement.className = 'mb-4';
    descriptionElement.textContent = description;
    resourceCard.appendChild(descriptionElement);

    // Create and append the 'Visit Site' text
    const visitSiteText = document.createElement('p');
    visitSiteText.className = 'text-brand-primary Hover:underline';
    visitSiteText.textContent = 'Visit Site';
    resourceCard.appendChild(visitSiteText);

    // Append the resource card to the anchor
    anchor.appendChild(resourceCard);

    // Append the anchor to the main div
    resourceItem.appendChild(anchor);

    return resourceItem;
}

// Example usage
const resources = [
    
    {
        group: 'Mental Health',
        link: 'https://www.samhsa.gov/find-help/national-helpline',
        title: 'SAMHSA’s National Helpline (1-800-662-4357)',
        description: 'A confidential, free, 24/7 service for individuals and families facing mental and substance use disorders.'
    },
    {
        group: 'Mental Health',
        link: 'https://988lifeline.org/',
        title: '988 Suicide and Crisis Lifeline',
        description: 'Provides 24/7, confidential support for people in distress, as well as prevention and crisis resources.'
    },
    {
        group: 'Mental Health',
        link: 'https://www.cdc.gov/mentalhealth/cope-with-stress/index.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fmentalhealth%2Fstress-coping%2Findex.html',
        title: 'Coping with Stress (CDC)',
        description: 'Offers strategies and resources for managing stress and improving mental health.'
    },
    {
        group: 'Mental Health',
        link: 'https://www.nami.org/about-nami/',
        title: 'National Alliance on Mental Illness (NAMI)',
        description: 'Provides education, support, and advocacy for individuals affected by mental illness.'
    },
    {
        group: 'ADHD',
        link: 'https://chadd.org/',
        title: 'CHADD',
        description: 'Children and Adults with Attention-Deficit/Hyperactivity Disorder (CHADD) is the leading non-profit organization providing support, education, and advocacy for individuals with ADHD.'
    },
    {
        group: 'ADHD',
        link: 'https://add.org/start/adda-resources/',
        title: 'Attention Deficit Disorder Association (ADDA)',
        description: 'The world\'s leading adult ADHD organization providing information, resources, and networking opportunities.'
    },
    {
        group: 'ADHD',
        link: 'https://github.com/XargsUK/awesome-adhd',
        title: 'Awesome ADHD',
        description: 'A curated list of ADHD apps, books, ideas, and resources across the web.'
    },
    {
        group: 'Autism',
        link: 'https://autisticadvocacy.org/',
        title: 'Autistic Self Advocacy Network (ASAN)',
        description: 'Run by and for autistic people, providing support, community, and advocacy.'
    },
    {
        group: 'Autism',
        link: 'https://awnnetwork.org/about/',
        title: 'Autistic Women & Nonbinary Network (AWN)',
        description: 'Supports and advocates for autistic women, girls, and nonbinary individuals.'
    },
    {
        group: 'Autism',
        link: 'https://a4aontario.com/about/',
        title: 'Autistics for Autistics (A4A Ontario)',
        description: 'A self-advocacy group by and for autistic adults in Ontario, Canada.'
    },
    {
        group: 'Autism',
        link: 'https://aaspire.org/',
        title: 'AASPIRE',
        description: 'Academic Autism Spectrum Partnership in Research and Education (AASPIRE) conducts research for the benefit of the autistic community.'
    },
    {
        group: 'Dyslexia',
        link: 'https://www.cde.ca.gov/ci/cr/dy/',
        title: 'Dyslexia - Curriculum and Instruction Resources (CA Dept of Education)',
        description: 'Provides resources and guidelines for educators to support students with dyslexia.'
    },
    {
        group: 'Dyslexia',
        link: 'https://ksmo.dyslexiaida.org/teacher-resources/',
        title: 'International Dyslexia Association',
        description: 'Promotes effective teaching approaches and related clinical educational intervention strategies for dyslexia.'
    },
    {
        group: 'Dyslexia',
        link: 'https://www.chconline.org/resourcelibrary/understanding-dyslexia/?utm_source=google_cpc&utm_medium=paid_search&utm_campaign=dsa&utm_term=&gad_source=1&gclid=CjwKCAjwtNi0BhA1EiwAWZaANNjGzJff96LK7I4K1BuqnVBU02LOfV1f7GJinn-4WPhCGkao58wFpRoCWI8QAvD_BwE',
        title: 'Children\'s Health Council - Understanding Dyslexia',
        description: 'Offers resources to help understand and manage dyslexia in children.'
    },
    {
        group: 'Dyslexia',
        link: 'https://opendyslexic.org/',
        title: 'OpenDyslexic Font',
        description: 'A free typeface designed to increase readability for readers with dyslexia.'
    },
    {
        group: 'Self-Advocacy',
        link: 'https://nacdd.org/self-advocacy-resources/',
        title: 'NACDD (National Association of Councils on Developmental Disabilities)',
        description: 'Advocates for inclusive federal and state public policies for people with developmental disabilities.'
    },
    {
        group: 'Self-Advocacy',
        link: 'https://selfadvocacyinfo.org/',
        title: 'SARTAC (Self Advocacy Resource and Technical Assistance Center)',
        description: 'Empowers individuals with disabilities to become effective self-advocates through resources and training.'
    },
    {
        group: 'Self-Advocacy',
        link: 'https://thearc.org/get-involved/self-advocacy/',
        title: 'The Arc - Self Advocacy Resources',
        description: 'Provides tools and information for self-advocates to help them understand and protect their rights.'
    },
    {
        group: 'Self-Advocacy',
        link: 'https://disabledteachersnetwork.weebly.com/uploads/9/8/7/7/9877420/pdf.pdf',
        title: 'Disability Rights California',
        description: 'Protects and advocates for the rights of Californians with disabilities.'
    },
    {
        group: 'Organization',
        link: 'https://www.theanimatedteacherblog.com/organizational-items-for-teachers/',
        title: '20 best organizational items for teachers ',
        description: ''
    },
    {
        group: 'Organization',
        link: 'https://www.fullspedahead.com/teacher-organization/',
        title: 'Teacher Organization Tips as a Special Ed Teacher',
        description: ''
    },
    {
        group: 'Organization',
        link: 'https://blog.prepscholar.com/teaching-tools-aids',
        title: '17 Great Teaching Tools for Organization, Assessment and More',
        description: ''
    },
    {
        group: 'All',
        link: 'static/files/article/neurodiversity-overview.jpg',
        title: 'Neurodiversity Infographic',
        description: 'Download Infographic'
    },
    {
        group: 'All',
        link: 'static/files/article/20 Classroom Management Tips (Overview).pdf',
        title: '20 Classroom Management Tips',
        description: 'Download Tips'
    },
    // Add more resources as needed
];

const resourceContainer = document.getElementById('resource-container');

resources.forEach(resource => {
    const resourceItem = createResourceItem(resource.group, resource.link, resource.title, resource.description);
    resourceContainer.appendChild(resourceItem);
});
